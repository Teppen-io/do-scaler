from functools import reduce
from statistics import median, mean


class Policy:
    reducer_map = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y
    }

    operator_map = {
        '<': lambda x, y: float(x) < float(y),
        '<=': lambda x, y: float(x) <= float(y),
        '>': lambda x, y: float(x) > float(y),
        '>=': lambda x, y: float(x) >= float(y),
        '==': lambda x, y: float(x) == float(y)
    }

    function_map = {
        'min': lambda n: min(n),
        'max': lambda n: max(n),
        'median': lambda n: median(n),
        'mean': lambda n: mean(n),
    }

    def __init__(self, config):
        self._set_attrs(config)

    def _set_attrs(self, config):
        for k, v in config.items():
            setattr(self, k, v)

    @staticmethod
    def _condition_satisfied(condition, values):
        val = Policy.function_map[condition['function']](values)
        return Policy.operator_map[condition['operator']](val, condition['threshold'])

    @staticmethod
    def _reduce_samples(condition, samples):
        val = reduce(Policy.reducer_map[condition['reducer']], samples) if len(samples) > 1 else samples[0]
        return val

    def _get_condition_values(self, condition):
        values = []
        for m in self._metrics:
            samples = []
            for sample in condition['samples']:
                samples.append(m.sample_value(sample['family'], sample['name']))
            values.append(self._reduce_samples(condition, samples))
        return values

    @property
    def _get_results(self):
        results = []
        for condition in self.conditions:
            values = self._get_condition_values(condition)
            satisfied = self._condition_satisfied(condition, values)
            results.append(satisfied)
        return results

    @property
    def _result_map(self):
        results = self._get_results
        return {
            'all': all(results),
            'any': any(results)
        }

    def satisfied(self, metrics):
        self._metrics = metrics
        return self._result_map[self.match]
