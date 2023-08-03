#ifndef __COREMEMDTM_H
#define __COREMEMDTM_H

#include <map>
#include <vector>
#include "drampolicy.h"
#include "dvfspolicy.h"
#include "performance_counters.h"

class coreMemDTM : public DramPolicy,public DVFSPolicy {
public:
    coreMemDTM(
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
        float dtmRecoveredMemTemperature);
    virtual std::map<int,int> getNewBankModes(std::map<int,int> old_bank_modes);
    virtual std::vector<int> getFrequencies(const std::vector<int> &oldFrequencies, const std::vector<bool> &activeCores);

private:
    const PerformanceCounters *performanceCounters;
    unsigned int numberOfCores;
    unsigned int numberOfBanks;
    int minFrequency;
    int maxFrequency;
    int frequencyStepSize;
    float upThreshold;
    float downThreshold;
    float dtmCriticalCoreTemperature;
    float dtmRecoveredCoreTemperature;
    float dtmCriticalMemTemperature;
    float dtmRecoveredMemTemperature;

 bool in_throttle_mode = false;
    bool throttle();
};

#endif

