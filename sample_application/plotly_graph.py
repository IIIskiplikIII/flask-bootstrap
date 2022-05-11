import json

import plotly
import plotly.graph_objects as go
import plotly.express as px


class PlotlyGraph:

    def __init__(self, x_col_name, y_col_name, color='blue') -> None:
        self.x_col_name = x_col_name
        self.y_col_name = y_col_name
        self.color = color

    
    def get_plotly_data(self, df):
        trace = px.scatter(df, x=self.x_col_name, y=self.y_col_name,
                        animation_frame="year", animation_group="country",
                        size="pop", color="continent", hover_name="country",
                        log_x=True, size_max=55, range_x=[100,100000], 
                        range_y=[25,90]
                        )
        return trace
    
    def get_json_graph(self,df):
        data = self.get_plotly_data(df)
        graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON