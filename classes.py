import pandas as pd
import plotly.graph_objects as go
class Graph:
    def __init__(self, title:str, xtitle:str, ytitle:str, names:list, kind:list, x:list, y:list, colors:list, styling:dict) -> None:
        """Stores all information for each graph and creates the composite figure for dash

        Note: the len of the kind, x, and y lists must match

        Args:
            title:      The title of the graph to be displayed on the webpage
            x/ytitle:   The title of the graph's x/y axes
            names:      A list of the titles for each subgraph
            kinds:      An ordered list of the types of the subgraphs (ex: bar, line, ...)
            xs:         A List of all x values as a pandas Series for each subgraph
            ys:         A List of all y valies as a pandas Series for each subgraph
            colors:     A List of all colors as a string for each subgraph
            styling:    A dict of all optional styling requirements (colors, clustered bars, etc)
        """
        self.title = title
        self.xtitle=xtitle
        self.ytitle=ytitle
        self.names = names
        self.type = kind
        self.x = x
        self.y = y
        self.styling = styling
    
    def buildFigure(self):
        fig_list = []
        for i in range(len(self.title)):
            if self.title[i] == "bar":
                fig_list.append(go.Bar(
                    name=self.names[i],
                    x=self.x,
                    y=self.y,
                    marker_color=self.styling["marker_colors"][i]
                ))
            elif self.title[i] == "line":
                fig_list.append(go.Scatter(
                    name=self.names[i],
                    x=self.x,
                    y=self.y,
                    marker_color=self.styling["marker_colors"][i]
                ))
        fig = go.Figure(fig_list)
        fig.update_layout(
            title=self.title,
            xaxis_title=self.xtitle,
            yaxis_title=self.ytitle
        )
        if self.styling.get("stackbars") == True:
            fig.update_layout(barmode='stack')
        return fig