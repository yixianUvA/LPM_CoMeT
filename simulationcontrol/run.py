import runlib
import sys, os

def example2():
    for benchmark in (
                      'parsec-blackscholes',
                      #'parsec-bodytrack',
                      #'parsec-canneal',
                      #'parsec-dedup',
                      #'parsec-fluidanimate',
                      #'parsec-streamcluster',
                      #'parsec-swaptions',
                      #'parsec-x264',
                      'splash2-barnes',
                      #'splash2-fmm',
                      'splash2-ocean.cont',
                      'splash2-ocean.ncont',
                      'splash2-radiosity',
                      'splash2-raytrace',
                      'splash2-water.nsq',
                      'splash2-water.sp',
                      'splash2-cholesky',
                      'splash2-fft',
                      'splash2-lu.cont',
                      'splash2-lu.ncont',
                      'splash2-radix'
                      ):
        min_parallelism = runlib.get_feasible_parallelisms(benchmark)[0]
        max_parallelism = runlib.get_feasible_parallelisms(benchmark)[-1]
        for freq in (1, 2, 3, 4):
            for parallelism in (min_parallelism, max_parallelism):
                # you can also use try_run instead
                runlib.run(['open', '{:.1f}GHz'.format(freq), 'constFreq'], runlib.get_instance(benchmark, parallelism, input_set='simsmall'))


def example():
    for freq in (1, 2, 3, 4):  # when adding a new frequency level, make sure that it is also added in base.cfg
        runlib.run(['open', '{:.1f}GHz'.format(freq), 'constFreq'], 'parsec-blackscholes-simmedium-15')

def case_study():
    fHz = ['4GHz']
    #bench = 'parsec-blackscholes'
    bench = 'parsec-x264'
    paral = 4
    for i in fHz:
        runlib.run([i,'2N','open', 'staticlow','low24'], runlib.get_instance(bench, parallelism=paral, input_set='simmedium'))
    for i in fHz:
        runlib.run([i,'4N','open', 'staticlow','low24'], runlib.get_instance(bench, parallelism=paral, input_set='simmedium'))
    for i in fHz:
        runlib.run([i,'8N','open', 'staticlow','low24'], runlib.get_instance(bench, parallelism=paral, input_set='simmedium'))
    for i in fHz:
        runlib.run([i,'16N','open', 'staticlow','low24'], runlib.get_instance(bench, parallelism=paral, input_set='simmedium'))
    for i in fHz:
        runlib.run([i,'32N','open', 'staticlow','low24'], runlib.get_instance(bench, parallelism=paral, input_set='simmedium'))
    for i in fHz:
        runlib.run([i,'48N','open', 'staticlow','low24'], runlib.get_instance(bench, parallelism=paral, input_set='simmedium'))
    runlib.run(['3.5GHz','open'], runlib.get_instance(bench, parallelism=paral, input_set='simmedium'))
    runlib.run(['3.7GHz','open'], runlib.get_instance(bench, parallelism=paral, input_set='simmedium'))


def testtest():
    fHz = '4.2GHz'
    bench = 'parsec-blackscholes'
    runlib.run([fHz,'32N','open', 'staticlow','low45'], runlib.get_instance(bench, parallelism=4, input_set='simsmall'))
    runlib.run([fHz,'16N','open', 'staticlow','low45'], runlib.get_instance(bench, parallelism=4, input_set='simsmall'))
    runlib.run([fHz,'open'], runlib.get_instance(bench, parallelism=4, input_set='simsmall'))
# def case_study():
#     runlib.run(['open', '5GHz'], runlib.get_instance('parsec-blackscholes', parallelism=4, input_set='small'))    


def date15():
    #fHz = '4GHz'
    for bench in (
                      'parsec-blackscholes',
                      'parsec-bodytrack',
                      'parsec-canneal',
                      'parsec-dedup',
                      'parsec-streamcluster',
                      'parsec-swaptions',
                      'parsec-x264',
                      ):
        runlib.run(['date15','open','d75'], runlib.get_instance(bench, parallelism=4, input_set='simmedium'))
    runlib.run(['date15','open','d75'], runlib.get_instance('parsec-fluidanimate', parallelism=3, input_set='simmedium'))
    
def lowpower():
    #fHz = '4GHz'
    for bench in (
                      'parsec-blackscholes',
                      'parsec-bodytrack',
                      'parsec-canneal',
                      'parsec-dedup',
                      'parsec-streamcluster',
                      'parsec-swaptions',
                      'parsec-x264',
                      ):
        runlib.run(['lowpower','open','low450','l75'], runlib.get_instance(bench, parallelism=4, input_set='simmedium'))
    runlib.run(['lowpower','open','low450','l75'], runlib.get_instance('parsec-fluidanimate', parallelism=3, input_set='simmedium'))
    
def CoreMemDTM():
    #fHz = '4GHz'
    for bench in (
                      'parsec-blackscholes',
                      'parsec-bodytrack',
                      'parsec-canneal',
                      'parsec-dedup',
                      'parsec-streamcluster',
                      'parsec-swaptions',
                      'parsec-x264',
                      ):
        runlib.run(['coreMemDTM','open','low24','cl75'], runlib.get_instance(bench, parallelism=4, input_set='simmedium'))
    runlib.run(['coreMemDTM','open','low24','cl75'], runlib.get_instance('parsec-fluidanimate', parallelism=3, input_set='simmedium'))


def date15_80():
    #fHz = '4GHz'
    for bench in (
                      'parsec-blackscholes',
                      'parsec-bodytrack',
                      'parsec-canneal',
                      'parsec-dedup',
                      'parsec-streamcluster',
                      'parsec-swaptions',
                      'parsec-x264',
                      ):
        runlib.run(['date15','open','d80'], runlib.get_instance(bench, parallelism=4, input_set='simmedium'))
    runlib.run(['date15','open','d80'], runlib.get_instance('parsec-fluidanimate', parallelism=3, input_set='simmedium'))
    
def lowpower_80():
    #fHz = '4GHz'
    for bench in (
                      'parsec-blackscholes',
                      'parsec-bodytrack',
                      'parsec-canneal',
                      'parsec-dedup',
                      'parsec-streamcluster',
                      'parsec-swaptions',
                      'parsec-x264',
                      ):
        runlib.run(['lowpower','open','low450','l80'], runlib.get_instance(bench, parallelism=4, input_set='simmedium'))
    runlib.run(['lowpower','open','low450','l80'], runlib.get_instance('parsec-fluidanimate', parallelism=3, input_set='simmedium'))
    
def CoreMemDTM_80():
    #fHz = '4GHz'
    for bench in (
                      'parsec-blackscholes',
                      'parsec-bodytrack',
                      'parsec-canneal',
                      'parsec-dedup',
                      'parsec-streamcluster',
                      'parsec-swaptions',
                      'parsec-x264',
                      ):
        runlib.run(['coreMemDTM','open','low24','cl80'], runlib.get_instance(bench, parallelism=4, input_set='simmedium'))
    runlib.run(['coreMemDTM','open','low24','cl80'], runlib.get_instance('parsec-fluidanimate', parallelism=3, input_set='simmedium'))

def date15_16():
    #fHz = '4GHz'
    for bench in (
                      'parsec-blackscholes',
                      'parsec-bodytrack',
                      'parsec-canneal',
                      'parsec-dedup',
                      'parsec-streamcluster',
                      'parsec-swaptions',
                      ):
        runlib.run(['date15','open','d80'], runlib.get_instance(bench, parallelism=16, input_set='simmedium'))
    runlib.run(['date15','open','d80'], runlib.get_instance('parsec-fluidanimate', parallelism=9, input_set='simmedium'))
    runlib.run(['date15','open','d80'], runlib.get_instance('parsec-x264',parallelism=9, input_set='simmedium'))
    
def lowpower_16():
    #fHz = '4GHz'
    for bench in (
                      'parsec-blackscholes',
                      'parsec-bodytrack',
                      'parsec-canneal',
                      'parsec-dedup',
                      'parsec-streamcluster',
                      'parsec-swaptions',
                      ):
        runlib.run(['lowpower','open','low450','l80'], runlib.get_instance(bench, parallelism=16, input_set='simmedium'))
    runlib.run(['lowpower','open','low450','l80'], runlib.get_instance('parsec-fluidanimate', parallelism=9, input_set='simmedium'))
    runlib.run(['lowpower','open','low450','l80'], runlib.get_instance('parsec-x264', parallelism=9, input_set='simmedium'))
    
def CoreMemDTM_16():
    #fHz = '4GHz'
    for bench in (
                      'parsec-blackscholes',
                      'parsec-bodytrack',
                      'parsec-canneal',
                      'parsec-dedup',
                      'parsec-streamcluster',
                      'parsec-swaptions',
                      ):
        runlib.run(['coreMemDTM','open','low24','cl80'], runlib.get_instance(bench, parallelism=16, input_set='simmedium'))
    runlib.run(['coreMemDTM','open','low24','cl80'], runlib.get_instance('parsec-fluidanimate',parallelism=9, input_set='simmedium'))
    runlib.run(['coreMemDTM','open','low24','cl80'], runlib.get_instance('parsec-x264',parallelism=9, input_set='simmedium'))
    
    
def date15_s():
    #fHz = '4GHz'
    for bench in (
                    'splash2-barnes',
                    #'splash2-fmm',
                    'splash2-ocean.cont',
                    'splash2-ocean.ncont',
                    'splash2-radiosity',
                    'splash2-raytrace',
                    'splash2-water.nsq',
                    'splash2-water.sp',
                    'splash2-cholesky',
                    'splash2-fft',
                    'splash2-lu.cont',
                    'splash2-lu.ncont',
                    'splash2-radix'
                      ):
        runlib.run(['date15','open','d75'], runlib.get_instance(bench, parallelism=4, input_set='large'))
    
def lowpower_s():
    #fHz = '4GHz'
    for bench in (
                    'splash2-barnes',
                    #'splash2-fmm',
                    'splash2-ocean.cont',
                    'splash2-ocean.ncont',
                    'splash2-radiosity',
                    'splash2-raytrace',
                    'splash2-water.nsq',
                    'splash2-water.sp',
                    'splash2-cholesky',
                    'splash2-fft',
                    'splash2-lu.cont',
                    'splash2-lu.ncont',
                    'splash2-radix'
                      ):
        runlib.run(['lowpower','open','low450','l75'], runlib.get_instance(bench, parallelism=4, input_set='large'))
    
def CoreMemDTM_s():
    #fHz = '4GHz'
    for bench in (
                    'splash2-barnes',
                    #'splash2-fmm',
                    'splash2-ocean.cont',
                    'splash2-ocean.ncont',
                    'splash2-radiosity',
                    'splash2-raytrace',
                    'splash2-water.nsq',
                    'splash2-water.sp',
                    'splash2-cholesky',
                    'splash2-fft',
                    'splash2-lu.cont',
                    'splash2-lu.ncont',
                    'splash2-radix'
                      ):
        runlib.run(['coreMemDTM','open','low24','cl75'], runlib.get_instance(bench, parallelism=4, input_set='large'))
        
def date15_ss():
    #fHz = '4GHz'
    for bench in (
                    'splash2-barnes',
                    #'splash2-fmm',
                    'splash2-ocean.cont',
                    'splash2-ocean.ncont',
                    'splash2-radiosity',
                    'splash2-raytrace',
                    'splash2-water.nsq',
                    'splash2-water.sp',
                    'splash2-cholesky',
                    'splash2-fft',
                    'splash2-lu.cont',
                    'splash2-lu.ncont',
                    'splash2-radix'
                      ):
        runlib.run(['date15','open','d75'], runlib.get_instance(bench, parallelism=16, input_set='large'))
    
def lowpower_ss():
    #fHz = '4GHz'
    for bench in (
                    'splash2-barnes',
                    #'splash2-fmm',
                    'splash2-ocean.cont',
                    'splash2-ocean.ncont',
                    'splash2-radiosity',
                    'splash2-raytrace',
                    'splash2-water.nsq',
                    'splash2-water.sp',
                    'splash2-cholesky',
                    'splash2-fft',
                    'splash2-lu.cont',
                    'splash2-lu.ncont',
                    'splash2-radix'
                      ):
        runlib.run(['lowpower','open','low450','l75'], runlib.get_instance(bench, parallelism=16, input_set='large'))
    
def CoreMemDTM_ss():
    #fHz = '4GHz'
    for bench in (
                    'splash2-barnes',
                    #'splash2-fmm',
                    'splash2-ocean.cont',
                    'splash2-ocean.ncont',
                    'splash2-radiosity',
                    'splash2-raytrace',
                    'splash2-water.nsq',
                    'splash2-water.sp',
                    'splash2-cholesky',
                    'splash2-fft',
                    'splash2-lu.cont',
                    'splash2-lu.ncont',
                    'splash2-radix'
                      ):
        runlib.run(['coreMemDTM','open','low24','cl75'], runlib.get_instance(bench, parallelism=16, input_set='large'))
        
def QUTM_s_16():
    #fHz = '4GHz'
    for bench in (
                    'splash2-barnes',
                    #'splash2-fmm',
                    'splash2-ocean.cont',
                    'splash2-ocean.ncont',
                    'splash2-radiosity',
                    'splash2-raytrace',
                    'splash2-water.nsq',
                    'splash2-water.sp',
                    'splash2-cholesky',
                    'splash2-fft',
                    'splash2-lu.cont',
                    'splash2-lu.ncont',
                    'splash2-radix'
                      ):
        runlib.run(['QU','open','low24','cl75'], runlib.get_instance(bench, parallelism=16, input_set='large'))
        
def QUTM_s_4():
    #fHz = '4GHz'
    for bench in (
                    'splash2-barnes',
                    #'splash2-fmm',
                    'splash2-ocean.cont',
                    'splash2-ocean.ncont',
                    'splash2-radiosity',
                    'splash2-raytrace',
                    'splash2-water.nsq',
                    'splash2-water.sp',
                    'splash2-cholesky',
                    'splash2-fft',
                    'splash2-lu.cont',
                    'splash2-lu.ncont',
                    'splash2-radix'
                      ):
        runlib.run(['QU','open','low24','cl75'], runlib.get_instance(bench, parallelism=4, input_set='large'))



def QUTM_p_16():
    #fHz = '4GHz'
    for bench in (
                      'parsec-blackscholes',
                      'parsec-bodytrack',
                      'parsec-canneal',
                      'parsec-dedup',
                      'parsec-streamcluster',
                      'parsec-swaptions',
                      ):
        runlib.run(['QU','open','low24','cl75'], runlib.get_instance(bench, parallelism=16, input_set='simmedium'))
    runlib.run(['QU','open','low24','cl75'], runlib.get_instance('parsec-fluidanimate',parallelism=9, input_set='simmedium'))
    runlib.run(['QU','open','low24','cl75'], runlib.get_instance('parsec-x264',parallelism=9, input_set='simmedium'))
    
def QUTM_p_4():
    #fHz = '4GHz'
    for bench in (
                      'parsec-blackscholes',
                      'parsec-bodytrack',
                      'parsec-canneal',
                      'parsec-dedup',
                      'parsec-streamcluster',
                      'parsec-swaptions',
                      'parsec-x264',
                      ):
        runlib.run(['QU','open','low24','cl75'], runlib.get_instance(bench, parallelism=4, input_set='simmedium'))
    runlib.run(['QU','open','low24','cl75'], runlib.get_instance('parsec-fluidanimate', parallelism=3, input_set='simmedium'))


def part(a,b):
    for i in range(a,b):
        runlib.run([str(i)+'N','4.2GHz','staticlow','low24','open'], runlib.get_instance('parsec-streamcluster',parallelism=4, input_set='simsmall'))
        #runlib.run([i+'N','4.2GHz',,'open', 'staticlow','low24'], runlib.get_instance(bench, parallelism=4, input_set='simsmall')
        
def date15_16():
    #fHz = '4GHz'
    for bench in (
                      'parsec-blackscholes',
                      'parsec-bodytrack',
                      'parsec-canneal',
                      'parsec-dedup',
                      'parsec-streamcluster',
                      'parsec-swaptions',
                      ):
        runlib.run(['date15','open','d75'], runlib.get_instance(bench, parallelism=16, input_set='simmedium'))
    runlib.run(['date15','open','d75'], runlib.get_instance('parsec-fluidanimate', parallelism=9, input_set='simmedium'))
    runlib.run(['date15','open','d75'], runlib.get_instance('parsec-x264',parallelism=9, input_set='simmedium'))
    
def lowpower_16():
    #fHz = '4GHz'
    for bench in (
                      'parsec-blackscholes',
                      'parsec-bodytrack',
                      'parsec-canneal',
                      'parsec-dedup',
                      'parsec-streamcluster',
                      'parsec-swaptions',
                      ):
        runlib.run(['lowpower','open','low450','l75'], runlib.get_instance(bench, parallelism=16, input_set='simmedium'))
    runlib.run(['lowpower','open','low450','l75'], runlib.get_instance('parsec-fluidanimate', parallelism=9, input_set='simmedium'))
    runlib.run(['lowpower','open','low450','l75'], runlib.get_instance('parsec-x264', parallelism=9, input_set='simmedium'))
    
def CoreMemDTM_16():
    #fHz = '4GHz'
    for bench in (
                      'parsec-blackscholes',
                      'parsec-bodytrack',
                      'parsec-canneal',
                      'parsec-dedup',
                      'parsec-streamcluster',
                      'parsec-swaptions',
                      ):
        runlib.run(['coreMemDTM','open','low24','cl75'], runlib.get_instance(bench, parallelism=16, input_set='simmedium'))
    runlib.run(['coreMemDTM','open','low24','cl75'], runlib.get_instance('parsec-fluidanimate',parallelism=9, input_set='simmedium'))
    runlib.run(['coreMemDTM','open','low24','cl75'], runlib.get_instance('parsec-x264',parallelism=9, input_set='simmedium'))    

def main():
    # CoreMemDTM_16()
    # lowpower_16()
    # date15_16()
    # QUTM_p_4()
    # QUTM_s_4()
    # QUTM_p_16()
    # QUTM_s_16()
    # date15_s()
    # lowpower_s()
    # CoreMemDTM_s()
    # date15_ss()
    # lowpower_ss()
    # CoreMemDTM_ss()
    
    


if __name__ == '__main__':
    main()
