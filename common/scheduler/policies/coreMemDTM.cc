#include "coreMemDTM.h"
#include <iomanip>
#include <iostream>
#include <map>
#include <vector>

using namespace std;

coreMemDTM::coreMemDTM(
        const PerformanceCounters *performanceCounters,
        int numberOfCores,
        int numberOfBanks,
        int minFrequency,
        int maxFrequency,
        int frequencyStepSize,
        float upThreshold,
        float downThreshold,
        float dtmCriticalCoreTemperature,
        float dtmRecoveredCoreTemperature,
        float dtmCriticalMemTemperature,
        float dtmRecoveredMemTemperature)
    : performanceCounters(performanceCounters),
      numberOfCores(numberOfCores),
      numberOfBanks(numberOfBanks),
      minFrequency(minFrequency),
      maxFrequency(maxFrequency),
      frequencyStepSize(frequencyStepSize),
      upThreshold(upThreshold),
      downThreshold(downThreshold),
      dtmCriticalCoreTemperature(dtmCriticalCoreTemperature),
      dtmRecoveredCoreTemperature(dtmRecoveredCoreTemperature),
      dtmCriticalMemTemperature(dtmCriticalMemTemperature),
      dtmRecoveredMemTemperature(dtmRecoveredMemTemperature) {

}

std::vector<int> coreMemDTM::getFrequencies(const std::vector<int> &oldFrequencies, const std::vector<bool> &activeCores) {
    if (throttle()) {
        std::vector<int> minFrequencies(numberOfCores, minFrequency);
        cout << "[Scheduler][core-DTM]: in throttle mode -> return min. frequencies" << endl;
        return minFrequencies;
    } else {
        std::vector<int> frequencies(numberOfCores);

        for (unsigned int coreCounter = 0; coreCounter < numberOfCores; coreCounter++) {
            if (activeCores.at(coreCounter)) {
                float power = performanceCounters->getPowerOfCore(coreCounter);
                float temperature = performanceCounters->getTemperatureOfCore(coreCounter);
                int frequency = oldFrequencies.at(coreCounter);
                float utilization = performanceCounters->getUtilizationOfCore(coreCounter);

                cout << "[Scheduler][core-DTM]: Core " << setw(2) << coreCounter << ":";
                cout << " P=" << fixed << setprecision(3) << power << " W";
                cout << "  f=" << frequency << " MHz";
                cout << "  T=" << fixed << setprecision(1) << temperature << " C";  // avoid the '°' symbol, it is not ASCII
                cout << "  utilization=" << fixed << setprecision(3) << utilization << endl;

                // use same period for upscaling and downscaling as described in "The ondemand governor."
                if (utilization > upThreshold) {
                    cout << "[Scheduler][core-DTM]: utilization > upThreshold";
                    if (frequency == maxFrequency) {
                        cout << " but already at max frequency" << endl;
                    } else {
                        cout << " -> go to max frequency" << endl;
                        frequency = maxFrequency;
                    }
                } else if (utilization < downThreshold) {
                    cout << "[Scheduler][core-DTM]: utilization < downThreshold";
                    if (frequency == minFrequency) {
                        cout << " but already at min frequency" << endl;
                    } else {
                        cout << " -> lower frequency" << endl;
                        frequency = frequency * 80 / 100;
                        frequency = (frequency / frequencyStepSize) * frequencyStepSize;  // round
                        if (frequency < minFrequency) {
                            frequency = minFrequency;
                        }
                    }
                }

                frequencies.at(coreCounter) = frequency;
            } else {
                frequencies.at(coreCounter) = minFrequency;
            }
        }

        return frequencies;
    }
}

bool coreMemDTM::throttle() {
    if (performanceCounters->getCorePeakTemperature() > dtmCriticalCoreTemperature) {
        if (!in_throttle_mode) {
            cout << "[Scheduler][core-DTM]: detected thermal violation" << endl;
        }
        in_throttle_mode = true;
    } else if (performanceCounters->getCorePeakTemperature() < dtmRecoveredCoreTemperature) {
        if (in_throttle_mode) {
            cout << "[Scheduler][core-DTM]: thermal violation ended" << endl;
        }
        in_throttle_mode = false;
    }
    return in_throttle_mode;
}

/*
Return the new memory modes, based on current temperatures.
*/
std::map<int,int> coreMemDTM::getNewBankModes(std::map<int, int> old_bank_modes) {

    cout << "in DramLowpower::getNewBankModes\n";
    std::map<int,int> new_bank_mode_map;
    for (int i = 0; i < numberOfBanks; i++)
    {
        if (old_bank_modes[i] == LOW_POWER) // if the memory was already in low power mode
        {
            if (performanceCounters->getTemperatureOfBank(i) < dtmRecoveredMemTemperature) // temp dropped below recovery temperature
            {
                cout << "[Scheduler][mem-DTM]: thermal violation ended for bank " << i << endl;
                new_bank_mode_map[i] = NORMAL_POWER;
            }
            else
            {
                new_bank_mode_map[i] = LOW_POWER;
            }
        }
        else // if the memory was not in low power mode
        {
            if (performanceCounters->getTemperatureOfBank(i) > dtmCriticalMemTemperature) // temp is above critical temperature
            {
                cout << "[Scheduler][mem-DTM]: thermal violation detected for bank " << i << endl;
                new_bank_mode_map[i] = LOW_POWER;
            }
            else
            {
                new_bank_mode_map[i] = NORMAL_POWER;
            }

        }
        
    }
    return new_bank_mode_map;
}