import collections
import diskcache
import gzip
import io
import os
import re
try:
    from config import RESULTS_FOLDER
except ImportError:
    from ..config import RESULTS_FOLDER

HERE = os.path.dirname(os.path.abspath(__file__))
RESULT_DIRS = [RESULTS_FOLDER]
NAME_REGEX = r'results_(\d+-\d+-\d+_\d+.\d+)_([a-zA-Z0-9_\.\+]*)_((splash2|parsec)-.*)'


cache = diskcache.Cache(directory=os.path.join(HERE, 'cache'))


def get_runs():
    for result_dir in RESULT_DIRS:
        if os.path.exists(result_dir):
            for dirname in os.listdir(result_dir):
                if dirname.startswith('results_'):
                    yield dirname


def find_run(run):
    for result_dir in RESULT_DIRS:
        candidate = os.path.join(result_dir, run)
        if os.path.exists(candidate):
            return candidate
    raise Exception('could not find run')


def _open_file(run, filename):
    for base_dir in RESULT_DIRS:
        full_filename = os.path.join(base_dir, run, filename)
        if os.path.exists(full_filename):
            return open(full_filename, 'r', encoding="utf-8")

        gzip_filename = '{}.gz'.format(full_filename)
        if os.path.exists(gzip_filename):
            return io.TextIOWrapper(gzip.open(gzip_filename, 'r'), encoding="utf-8")
    raise Exception('file does not exist')


def get_date(run):
    m = re.search(NAME_REGEX, run)
    return m.group(1)


def get_config(run):
    m = re.search(NAME_REGEX, run)
    return m.group(2)


def get_tasks(run):
    m = re.search(NAME_REGEX, run)
    tasks = m.group(3).split(',')
    return ', '.join(t[t.find('-')+1:] for t in tasks)


def has_properly_finished(run):
    return get_average_response_time(run) is not None



@cache.memoize()
def get_total_simulation_time(run):
    with _open_file(run, 'sim.out') as f:
        for line in f:
            tokens = line.split()
            if tokens[0] == 'Time':
                return int(tokens[3])
    return '-'


def get_dram_read_access(run):
    n_dram_access = [0 for i in range(128)]
    with _open_file(run, 'execution.log') as f:
        for line in f:
            m = re.search(r'\[STAT:dram.bank_read_access_counter\]\s+([\d\s]+)',line)
            if m is not None:
                data = m.group(1).split()
                data = [int(x) for x in data]
                for i in range(128):
                    n_dram_access[i] += data[i]
        print(n_dram_access)
        return n_dram_access
    
def get_avg_dram_read_per_bank(run):
    n_dram_access = [0 for i in range(128)]
    count = 0
    with _open_file(run, 'execution.log') as f:
        for line in f:
            m = re.search(r'\[STAT:dram.bank_read_access_counter\]\s+([\d\s]+)',line)
            if m is not None:
                count += 1
                data = m.group(1).split()
                data = [int(x) for x in data]
                for i in range(128):
                    n_dram_access[i] += data[i]
        nn_dram_access = [i / count for i in n_dram_access]
        print('dram_access',len(n_dram_access))
        print('nn_dram_access',len(nn_dram_access))
        
        return nn_dram_access
    
def get_dram_write_access(run):
    n_dram_access = [0 for i in range(128)]
    with _open_file(run, 'execution.log') as f:
        for line in f:
            m = re.search(r'\[STAT:dram.bank_write_access_counter\]\s+([\d\s]+)',line)
            if m is not None:
                data = m.group(1).split()
                data = [int(x) for x in data]
                for i in range(128):
                    n_dram_access[i] += data[i]
        print(n_dram_access)
        return n_dram_access
    
def get_avg_dram_write_access_per_bank(run):
    n_dram_access = [0 for i in range(128)]
    count = 0 
    with _open_file(run, 'execution.log') as f:
        for line in f:
            m = re.search(r'\[STAT:dram.bank_write_access_counter\]\s+([\d\s]+)',line)
            if m is not None:
                count += 1
                data = m.group(1).split()
                data = [int(x) for x in data]
                for i in range(128):
                    n_dram_access[i] += data[i]
        nn_dram_access = [i / count for i in n_dram_access]
        #print(nn_dram_access)
        return nn_dram_access
                #return 0
            #return m.group(0)

@cache.memoize()
def get_average_response_time(run):
    with _open_file(run, 'execution.log') as f:
        for line in f:
            m = re.search(r'Average Response Time \(ns\)\s+:\s+(\d+)', line)
            if m is not None:
                #print("m.group(0) is ",m.group(0))
                return int(m.group(1))
            

#@cache.memoize()
def get_violent_memory_bank(run):
    with _open_file(run, 'execution.log') as f:
        vio_list = []
        for line in f:
            m = re.search(r'\[Scheduler\]\[dram-DTM\]: thermal violation ended for bank (\d+)', line);
            if m is not None:
                vio_list.append(int(m.group(1)))
        # print(vio_list)
        # print(len(vio_list))
        lay_list = []
        for i in range (0,len(vio_list)):
            #lay_list.append(int(vio_list[i] / 16))
            lay_list.append(int(vio_list[i]))
        #print(lay_list)
        set_list = set(lay_list)
        #print(set_list)
        temp = {}
        for i in set_list:
            temp_cout = 0;
            for j in lay_list:  
                if i == j:
                    temp_cout += 1
            temp[i] = temp_cout
            #count_list.append(temp)
        print(temp)
        for key,value in temp.items():
            print('The memory bank {layer} overshoot {times} times'.format(layer=key,times=value))
                

@cache.memoize()
def get_individual_response_times(run):
    resp_times = {}
    with _open_file(run, 'execution.log') as f:
        for line in f:
            m = re.search(r'Task (\d+) \(Response/Service/Wait\) Time \(ns\)\s+:\s+(\d+)\s+(\d+)\s+(\d+)', line)
            if m is not None:
                task = int(m.group(1))
                resp = int(m.group(2))
                resp_times[task] = resp
    keys = sorted(resp_times.keys())
    if len(keys) == 0:
        return '-'
    elif keys != list(range(max(keys)+1)):
        raise Exception('task(s) missing: {}'.format(', '.join(map(str, sorted(list(set(range(max(keys)+1)) - set(keys)))))))
    else:
        return [resp_times[task] for task in keys]
    
@cache.memoize()
def get_individual_start_times(run):
    start_times = {}
    with _open_file(run, 'execution.log') as f:
        for line in f:
            m = re.search(r'\[Scheduler\]: Trying to schedule Task (?P<task>\d+) at Time (?P<time>\d+) ns', line)
            if m is not None:
                task = int(m.group('task'))
                t = int(m.group('time'))
                start_times[task] = t
    start_keys = sorted(start_times.keys())
    if start_keys == []:
        raise Exception('task(s) missing (non found)')
    elif start_keys != list(range(max(start_keys)+1)):
        raise Exception('task(s) missing')
    else:
        return [start_times[task] for task in start_keys]

def avg(data):
    return float(sum(data)) / len(data)

def get_power_traces(run):
    return _get_traces(run, 'full_power_core.trace')

def get_m_power_traces(run):
    return _get_traces(run, 'full_power_mem.trace')


@cache.memoize()
def get_average_power_consumption(run):
    traces = get_power_traces(run)
    power_values = [sum(ps) for ps in zip(*traces)]
    return avg(power_values)

@cache.memoize()
def get_energy(run):
    power = get_average_power_consumption(run)
    simulation_time = get_total_simulation_time(run)
    if simulation_time in ('-',):
        return '-'
    time = simulation_time / 1e9
    return power * time


# @cache.memoize()
# def get_individual_energies(run):
#     """
#     get energy consumption per task
#     """
#     start_times = get_individual_start_times(run)
#     response_times = get_individual_response_times(run)
#     end_times = [start_times[i] + response_times[i] for i in range(len(start_times))]
#     traces = get_power_traces(run)
#     power_values = [sum(ps) for ps in zip(*traces)]

#     energies = [0] * len(start_times)

#     dt = 100000
#     for i, p in enumerate(power_values):
#         t = i * dt
#         active_tasks = [i for i in range(len(start_times)) if start_times[i] <= t and end_times[i] > t]
#         for t in active_tasks:
#             energies[t] += p / len(active_tasks) * dt / 1e9

#     # double check
#     assert abs(sum(energies) - get_energy(run)) < 0.01, '{:.2f} != {:.2f}'.format(sum(energies), get_energy(run))
#     return energies

def get_memory_peak_temperature_traces(run, level):
    header = _get_header(run, 'combined_temperature.trace')
    assert all(h.startswith('B') for h in header[count_cores(run):])  # simple check for order or header
    traces = _get_traces(run, 'combined_temperature.trace')
    temp = traces[0:4]
    if level > 0:
        temp = traces[level*8:(level+1)*8]
    peak = []
    # print(len(temp))
    # print(temp)
    # print(count_cores(run))
    for values in zip(*temp):
        peak.append(max(values))
    #return collections.OrderedDict((h, t) for h, t in zip(["M_L"+str(level)], [peak]))
    return peak

def get_memory_peak_temperaure(run):
    header = _get_header(run, 'combined_temperature.trace')
    assert all(h.startswith('B') for h in header[count_cores(run):])  # simple check for order or header
    traces = _get_traces(run, 'combined_temperature.trace')
    collectPeak = []
    real_peak = []
    for i in range(1,9):
        temp = traces[i*8:(i+1)*8]
        peak = []
        for values in zip(*temp):
            peak.append(max(values))
        collectPeak.append(peak)
    for value in zip(*collectPeak):
        real_peak.append(max(value))
    return real_peak


@cache.memoize()
def get_energy(run):
    power = get_average_power_consumption(run)
    simulation_time = get_total_simulation_time(run)
    if simulation_time in ('-',):
        return '-'
    time = simulation_time / 1e9
    return power * time
 
#@cache.memoize()
def get_individual_energies(run):
    """
    get energy consumption per task
    """
    start_times = get_individual_start_times(run)
    response_times = get_individual_response_times(run)
    end_times = [start_times[i] + response_times[i] for i in range(len(start_times))]
    traces = get_power_traces(run)
    #print(len(traces))
    power_values = [sum(ps) for ps in zip(*traces)]

    #energies = [0] * len(start_times)
    #print('The power value of power_values are ', len(power_values))
    #print(power_values[0])
    #dt = 100000
    dt = 1000
    energy = 0
    for i in power_values:
        energy += i/dt
        
    trace1 = get_m_power_traces(run)
    power_values1 = [sum(ps) for ps in zip(*trace1)]
    energy1 = 0
    for i in power_values1:
        energy1 += i/dt
    #print('***', ' ', energy,'   ', energy1)
    return energy + energy1  
    # for i, p in enumerate(power_values):
    #     t = i * dt
    #     active_tasks = [i for i in range(len(start_times)) if start_times[i] <= t and end_times[i] > t]
    #     print('active_tasks',active_tasks)
    #     #print('The size of active_tasks are ', len(active_tasks))
    #     for t in active_tasks:
    #         energies[t] += p / len(active_tasks) * dt / 1e9
    #         #print()
    
    # # print("*************")
    # # print(sum(energies))
    # # print("----***********")
    
    # #assert 0
    # #double check
    # #assert abs(sum(energies) * 10 - get_energy(run)) < 0.01, '{:.2f} != {:.2f}'.format(sum(energies), get_energy(run))
    # return get_energy(run)


def _get_traces(run, filename, multiplicator=1):
    traces = []

    with _open_file(run, filename) as f:
        f.readline()
        for line in f:
            vs = [multiplicator * float(v) for v in line.split()]
            traces.append(vs)

    return list(zip(*traces))


def _get_header(run, filename):
    with _open_file(run, filename) as f:
        header = f.readline().split()
    return header


def _get_named_traces(run, filename, multiplicator=1):
    traces = []

    with _open_file(run, filename) as f:
        header = f.readline().split()
        for line in f:
            vs = [multiplicator * float(v) for v in line.split()]
            traces.append(vs)
    traces = list(zip(*traces))

    return collections.OrderedDict((h, t) for h, t in zip(header, traces))


def get_core_power_traces(run):
    header = _get_header(run, 'combined_power.trace')
    assert all(h.startswith('C') for h in header[:count_cores(run)])  # simple check for order or header
    traces = _get_traces(run, 'combined_power.trace')
    return traces[:count_cores(run)]


def get_memory_power_traces(run):
    header = _get_header(run, 'combined_power.trace')
    assert all(h.startswith('B') for h in header[count_cores(run):])  # simple check for order or header
    traces = _get_traces(run, 'combined_power.trace')
    return traces[count_cores(run):]

def get_combined_power_trace(run):
    # header = _get_header(run, 'combined_power.trace')
    # assert all(h.startswith('B') or h.startswith('C') for h in header[count_cores(run):])  # simple check for order or header
    traces = _get_traces(run, 'combined_power.trace')
    return traces
    


def get_core_temperature_traces(run):
    header = _get_header(run, 'combined_temperature.trace')
    assert all(h.startswith('C') for h in header[:count_cores(run)])  # simple check for order or header
    traces = _get_traces(run, 'combined_temperature.trace')
    return traces[:count_cores(run)]


def get_memory_temperature_traces(run):
    header = _get_header(run, 'combined_temperature.trace')
    assert all(h.startswith('B') for h in header[count_cores(run):])  # simple check for order or header
    traces = _get_traces(run, 'combined_temperature.trace')
    return traces[count_cores(run):]


def get_core_peak_temperature_traces(run):
    traces = get_core_temperature_traces(run)
    peak = []
    for values in zip(*traces):
        peak.append(max(values))
    return [peak]


def get_core_peak_temperature(run):
    return max(max(get_core_peak_temperature_traces(run)))

def get_mem_peak_temperature(run):
    return max(max(get_mem_peak_temperature_traces(run)))

def get_mem_peak_temperature_traces(run):
    traces = get_memory_temperature_traces(run)
    peak = []
    for values in zip(*traces):
        peak.append(max(values))
    return [peak]


def get_all_temperature_traces(run):
    traces = _get_named_traces(run, 'combined_temperature.trace')
    return traces

def get_all_power_traces(run):
    traces = _get_named_traces(run, 'combined_power.trace')
    return traces


def get_peak_temperature(run):
   a = max(max(get_core_peak_temperature_traces(run)))
   b = max(max(get_mem_peak_temperature_traces(run)))
   return max(a,b)
   


@cache.memoize()
def get_cpi_stack_trace_parts(run):
    parts = []
    with _open_file(run, 'PeriodicCPIStack.log') as f:
        f.readline()
        for line in f:
            part = line.split()[0]
            if part not in parts:
                parts.append(part)
    assert len(parts) > 0, 'empty PeriodicCPIStack.log'
    return parts


def get_cpi_stack_part_trace(run, part='total'):
    traces = []

    trace_values = []
    with _open_file(run, 'PeriodicCPIStack.log') as f:
        f.readline()
        for line in f:
            if line.startswith(part + '\t'):
                items = line.split()[1:]
                if items == ['-']:
                    ps = [0] * count_cores(run)
                else:
                    ps = [float(value) for value in items]
                trace_values.append(ps)

    return list(zip(*trace_values))


def _add_traces(trace1, trace2):
    assert len(trace1) == len(trace2), 'number of cores differs: {} != {}'.format(len(trace1), len(trace2))
    traces = []
    for t1, t2 in zip(trace1, trace2):
        assert len(t1) == len(t2), 'length of traces differ: {} != {}'.format(len(t1), len(t2))
        traces.append([v1 + v2 for v1, v2 in zip(t1, t2)])
    return traces


def _divide_traces(numerator, denominator):
    assert len(numerator) == len(denominator), 'number of cores differs: {} != {}'.format(len(numerator), len(denominator))
    traces = []
    for num, den in zip(numerator, denominator):
        assert len(num) == len(den), 'length of traces differ: {} != {}'.format(len(num), len(den))
        traces.append([n / d if d != 0 else None for n, d in zip(num, den)])
    return traces


def get_ips_traces(run):
    return _divide_traces(get_core_freq_traces(run), get_cpi_traces(run, raw=True))


def get_cpi_traces(run, raw=False):
    traces = list(map(list, get_cpi_stack_part_trace(run, 'total')))
    if not raw:
        w = 2
        for trace in traces:
            drop = [i for i in range(len(trace)) if any(t > 20 for t in trace[max(i-w,0):min(i+w,len(trace))])]
            for i in drop:
                trace[i] = None
    return traces


def get_core_freq_traces(run):
    return _get_traces(run, 'PeriodicFrequency.log', multiplicator=1e9)


def get_core_utilization_traces(run):
    cpi = None
    for part in get_cpi_stack_trace_parts(run):
        blacklist = ['total', 'mem', 'ifetch', 'sync', 'dvfs-transition', 'imbalance', 'other']
        if all(b not in part for b in blacklist):
            part_trace = get_cpi_stack_part_trace(run, part)
            if cpi is None:
                cpi = part_trace
            else:
                cpi = _add_traces(cpi, part_trace)
    assert cpi is not None, 'no valid CPI stack parts found to calculate utilization'
    return _divide_traces(cpi, get_cpi_stack_part_trace(run, 'total'))


@cache.memoize()
def count_cores(run):
    return len(get_core_freq_traces(run))


@cache.memoize()
def get_active_cores(run):
    utilization_traces = get_core_utilization_traces(run)
    return [i for i, utilization in enumerate(utilization_traces) if max(utilization) > 0.01]
