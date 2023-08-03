#include "dramStaticLow.h"
#include <iomanip>
#include <iostream>
#include <map>

using namespace std;

DramStaticLow::DramStaticLow(
        const PerformanceCounters *performanceCounters,
        int numberOfBanks,
        float dtmCriticalTemperature,
        float dtmRecoveredTemperature,
        float off_bank_number)
    : performanceCounters(performanceCounters),
      numberOfBanks(numberOfBanks),
      dtmCriticalTemperature(dtmCriticalTemperature),
      dtmRecoveredTemperature(dtmRecoveredTemperature),
      off_bank_number(off_bank_number) {

}

/*
Return the new memory modes, based on current temperatures.
*/
std::map<int,int> DramStaticLow::getNewBankModes(std::map<int, int> old_bank_modes) {

    cout << "in DramStaticLow::getNewBankModes\n";
    std::map<int,int> new_bank_mode_map;
    //std::cout << "*****&&&&&&The number of banks is " << numberOfBanks << std::endl;
    for (int i = 0; i < numberOfBanks; i++)
    {
        if(i == off_bank_number){
            cout << "[Scheduler][dram-StaticLow]: putting memory bank to low power mode" << i << endl;
            new_bank_mode_map[i] = LOW_POWER;
        }
        else
            {
                new_bank_mode_map[i] = NORMAL_POWER;
            }
       
    }
       
    return new_bank_mode_map;
}