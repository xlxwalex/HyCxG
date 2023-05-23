import abc
import copy
import datetime
import math
import pickle
import random
import signal
import sys
import time

def round_figures(x, n):
    """Returns x rounded to n significant figures."""
    return round(x, int(n - math.ceil(math.log10(abs(x)))))


def time_string(seconds):
    """Returns time in seconds as a string formatted HHHH:MM:SS."""
    s = int(round(seconds))  # round to nearest second
    h, s = divmod(s, 3600)   # get hours and remainder
    m, s = divmod(s, 60)     # split remainder into minutes and seconds
    return '%4i:%02i:%02i' % (h, m, s)


class Annealer(object):
    __metaclass__ = abc.ABCMeta
    # defaults
    Tmax = 25000.0
    Tmin = 2.5
    steps = 50000
    updates = 100
    copy_strategy = 'deepcopy'
    user_exit = False
    save_state_on_exit = False
    T = None
    vis_status = False

    # placeholders
    best_state = None
    best_energy = None
    start = None

    def __init__(self, initial_state=None, vis=False, load_state=None):
        self.vis_status = vis
        if initial_state is not None:
            self.state = self.copy_state(initial_state)
        elif load_state:
            self.load_state(load_state)
        else:
            raise ValueError('No valid values supplied for neither \
            initial_state nor load_state')

        signal.signal(signal.SIGINT, self.set_user_exit)

    def save_state(self, fname=None):
        """Saves state to pickle"""
        if not fname:
            date = datetime.datetime.now().strftime("%Y-%m-%dT%Hh%Mm%Ss")
            fname = date + "_energy_" + str(self.energy()) + ".state"
        with open(fname, "wb") as fh:
            pickle.dump(self.state, fh)

    def load_state(self, fname=None):
        """Loads state from pickle"""
        with open(fname, 'rb') as fh:
            self.state = pickle.load(fh)

    @abc.abstractmethod
    def move(self):
        """Create a state change"""
        pass

    @abc.abstractmethod
    def energy(self):
        """Calculate state's energy"""
        pass

    def set_user_exit(self, signum, frame):
        self.user_exit = True

    def set_schedule(self, schedule):
        self.Tmax = schedule['tmax']
        self.Tmin = schedule['tmin']
        self.steps = int(schedule['steps'])
        self.updates = int(schedule['updates'])

    def copy_state(self, state):
        if self.copy_strategy == 'deepcopy':
            return copy.deepcopy(state)
        elif self.copy_strategy == 'slice':
            return state[:]
        elif self.copy_strategy == 'method':
            return state.copy()
        else:
            raise RuntimeError('No implementation found for ' +
                               'the self.copy_strategy "%s"' %
                               self.copy_strategy)

    def update(self, *args, **kwargs):
        self.default_update(*args, **kwargs)

    def default_update(self, step, T, E, acceptance, improvement):
        elapsed = time.time() - self.start
        if step == 0:
            if self.vis_status:
                print('\n Temperature        Energy    Accept   Improve     Elapsed   Remaining',
                      file=sys.stderr)
                print('\r{Temp:12.5f}  {Energy:12.2f}                      {Elapsed:s}            '
                      .format(Temp=T,
                              Energy=E,
                              Elapsed=time_string(elapsed)),
                      file=sys.stderr, end="")
                sys.stderr.flush()
        else:
            if self.vis_status:
                remain = (self.steps - step) * (elapsed / step)
                print('\r{Temp:12.5f}  {Energy:12.2f}   {Accept:7.2%}   {Improve:7.2%}  {Elapsed:s}  {Remaining:s}'
                      .format(Temp=T,
                              Energy=E,
                              Accept=acceptance,
                              Improve=improvement,
                              Elapsed=time_string(elapsed),
                              Remaining=time_string(remain)),
                      file=sys.stderr, end="")
                sys.stderr.flush()

    def anneal(self):
        step = 0
        self.start = time.time()
        if self.Tmin <= 0.0:
            raise Exception('Exponential cooling requires a minimum "\
                "temperature greater than zero.')
        Tfactor = -math.log(self.Tmax / self.Tmin)

        self.T = self.Tmax
        E = self.energy()
        prevState = self.copy_state(self.state)
        prevEnergy = E
        self.best_state = self.copy_state(self.state)
        self.best_energy = E
        trials = accepts = improves = 0
        if self.updates > 0:
            updateWavelength = self.steps / self.updates
            self.update(step, self.T, E, None, None)
        while step < self.steps and not self.user_exit:
            step += 1
            self.T = self.Tmax * math.exp(Tfactor * step / self.steps)
            dE = self.move()
            if dE is None:
                E = self.energy()
                dE = E - prevEnergy
            else:
                E += dE
            trials += 1
            if dE > 0.0 and math.exp(-dE / self.T) < random.random():
                self.state = self.copy_state(prevState)
                E = prevEnergy
            else:
                accepts += 1
                if dE < 0.0:
                    improves += 1
                prevState = self.copy_state(self.state)
                prevEnergy = E
                if E < self.best_energy:
                    self.best_state = self.copy_state(self.state)
                    self.best_energy = E
            if self.updates > 1:
                if (step // updateWavelength) > ((step - 1) // updateWavelength):
                    self.update(
                        step, self.T, E, accepts / trials, improves / trials)
                    trials = accepts = improves = 0

        self.state = self.copy_state(self.best_state)
        if self.save_state_on_exit:
            self.save_state()
        return self.best_state, self.best_energy

    def auto(self, minutes, steps=2000):
        def run(T, steps):
            E = self.energy()
            prevState = self.copy_state(self.state)
            prevEnergy = E
            accepts, improves = 0, 0
            for _ in range(steps):
                dE = self.move()
                if dE is None:
                    E = self.energy()
                    dE = E - prevEnergy
                else:
                    E = prevEnergy + dE
                if dE > 0.0 and math.exp(-dE / T) < random.random():
                    self.state = self.copy_state(prevState)
                    E = prevEnergy
                else:
                    accepts += 1
                    if dE < 0.0:
                        improves += 1
                    prevState = self.copy_state(self.state)
                    prevEnergy = E
            return E, float(accepts) / steps, float(improves) / steps

        step = 0
        self.start = time.time()

        self.T = 0.0
        E = self.energy()
        self.update(step, self.T, E, None, None)
        while self.T == 0.0:
            step += 1
            dE = self.move()
            if dE is None:
                dE = self.energy() - E
            self.T = abs(dE)

        E, acceptance, improvement = run(self.T, steps)

        step += steps
        while acceptance > 0.98:
            self.T = round_figures(self.T / 1.5, 2)
            E, acceptance, improvement = run(self.T, steps)
            step += steps
            self.update(step, self.T, E, acceptance, improvement)
        while acceptance < 0.98:
            self.T = round_figures(self.T * 1.5, 2)
            E, acceptance, improvement = run(self.T, steps)
            step += steps
            self.update(step, self.T, E, acceptance, improvement)
        Tmax = self.T
        while improvement > 0.0:
            self.T = round_figures(self.T / 1.5, 2)
            E, acceptance, improvement = run(self.T, steps)
            step += steps
            self.update(step, self.T, E, acceptance, improvement)
        Tmin = self.T
        elapsed = time.time() - self.start
        duration = round_figures(int(60.0 * minutes * step / elapsed), 2)
        return {'tmax': Tmax, 'tmin': Tmin, 'steps': duration, 'updates': self.updates}