import figures.NetworkTrafficStats as nts1
import figures.NetworkThreatStats as nts2
import figures.AllowedThreats as at
import figures.TotalNetworkStats as tns
import figures.AllEventsGraph as ae
import figures.TableTotalStats as tts
import figures.HostExploitDetectionStats as heds
import figures.SplunkIndexStats as sis
import figures.HostThreatQuarantined as htq
import figures.TableForAllTotals as tfat

def get():
    return [
        [nts1, nts2], 
        [at, tns], 
        [ae, tts], 
        [sis, None], 
        [heds, htq],
        [tfat]
    ]