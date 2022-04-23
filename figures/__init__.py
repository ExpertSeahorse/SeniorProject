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
    """Get all graph modules in order"""
    return [
        [nts1, nts2], 
        [at, tns], 
        [ae, tts], 
        [sis, None], 
        [heds, htq],
        [tfat]
    ]

import plotly.graph_objects as go
def getThemes():
    """Get light and dark theme modifications"""
    lightmode = go.layout.Template(layout_paper_bgcolor='rgba(0,0,0,0)')
    lightmode.data.table = [go.Table(
        header={'fill_color': 'lightskyblue', 'align': 'center'},
        cells={'align': 'center'}
    )]
    darkmode = go.layout.Template(layout_paper_bgcolor='rgba(0,0,0,0)')

    darkmode.data.table = [go.Table(
        header={'fill_color': 'SteelBlue', 'align': 'center'},
        cells={'align': 'center'}
    )]
    return lightmode, darkmode