# Imports
from ensurepip import bootstrap
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio
import pickle
import json
import numpy as np
from .problem_description import Problem
from .plot_functions import plot_selected_watersheds, \
    plot_selected_contourlines, \
    swc_allocation_create_background_map,\
    swc_allocation_layout, plot_selected_landuse_map


def init_pareto3(server):

    # Classes
    class Solution:

        _id = 0

        def __init__(self, representation, objective_values):
            self._solution_id = Solution._id
            Solution._id += 1
            self.representation = representation
            self.objective_values = objective_values

    #defs
    def blank_figure():
        fig = go.Figure(go.Scatter(x=[], y=[]))
        fig.update_layout(template=None)
        fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
        fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
        return fig

    def create_layout():
        # Actual layout of the dash_app
        return html.Div(
            id="root",
            children=[
                html.Div(
                    id="app-container",
                    children=[
                        html.Div(
                            id="left-column",
                            children=[
                                dcc.Interval(
                                    id="load_interval",
                                    n_intervals = 0,
                                    max_intervals = 0, # <- only run once
                                    interval = 1
                                ),
                                    html.Div(
                                    id="pareto_front-container",
                                    children=[
                                        dcc.Graph(
                                            id="pareto_front", style={"display": "inline-block" , "height": "50vh", "width": "60vh"}
                                        ),
                                        dcc.Graph(
                                            id="selected_data", style={"display": "inline-block" , "height": "50vh", "width": "60vh"}
                                        )
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    def interactiveParetoFront(dash_app, problem, save_front = None):

        def generate_figure_image(figure, points,layout, opacity):
            figure.add_trace(go.Scatter(
                x=points.iloc[:, 0],
                y=points.iloc[:, 1],
                showlegend=True,
                legendgroup="scatterpoints",
                textposition="top left",
                mode="markers",
                marker=dict(size=3, symbol="circle", opacity=opacity),

            ),
                secondary_y=False,
            )

            return figure
        @dash_app.callback(
            Output("pareto_front", "figure"),
            Input("load_interval", "n_intervals")
        )
        def display_scatter_plot(n_intervals):

            axes = dict(title="", showgrid=True, zeroline=False, showticklabels=False)
            layout = go.Layout(
                xaxis_title=problem.objective_names[0],
                yaxis_title=problem.objective_names[1],
                font=dict(
                    family="Bodoni Moda",
                    size=14
                )

            )
            figure = go.Figure(layout=layout)
            figure = make_subplots(figure=figure)

            i = 0
            obj1_values = []
            obj2_values = []
            solution_ids = []
            for pareto_front in problem.benchmarks:
                for solution in pareto_front:
                    for realization_id in range(len(solution.objective_values[0])):
                        obj1_values.append(solution.objective_values[0][realization_id])
                        obj2_values.append(solution.objective_values[1][realization_id])
                        solution_ids.append(i)
                    i += 1
            scattered_points = pd.DataFrame(
                {'obj1': np.array(obj1_values), 'obj2': np.array(obj2_values), 'sol_id': np.array(solution_ids)})
            plot_mode = "scatter"

            if plot_mode == 'scatter':
                figure = generate_figure_image(figure, scattered_points, layout, opacity=1)

            names = set()
            figure.for_each_trace(
                lambda trace:
                trace.update(showlegend=False)
                if (trace.name in names) else names.add(trace.name))

            #save figure
            if save_front is not None:
                ppi = 96
                width_cm = 3
                height_cm = 2
                pio.write_image(figure, os.path.join(save_front, "pf.svg"),
                                width=(width_cm * 2.54) * ppi,
                                height=(height_cm * 2.54) * ppi)
            return figure

        @dash_app.callback(
            Output("selected_data", "figure"),
            [
                Input("pareto_front", "clickData"),
            ],
        )
        ## in brief: get the position of the point in the plot that you click on and find
        # the solution with the corresponding objective values. When its found, select the solution representation
        # and plot it.
        def display_click_image(clickData):
            if clickData:
                print(clickData)
                clicked_solution = None
                click_point_np = [float(clickData["points"][0][i]) for i in ["x", "y"]]

                filtered_solutions = []
                for pareto_front in problem.benchmarks:
                    for solution in pareto_front:
                        filtered_solutions.append(solution)
                        if click_point_np[0] in solution.objective_values[0] and \
                                click_point_np[1] in solution.objective_values[1]:
                            clicked_solution = solution
                try:
                    if clickData and clicked_solution is not None:
                        layout1 = go.Layout(
                            #title=f'Corresponding solution',
                            yaxis=dict(showticklabels=False),
                            xaxis=dict(showticklabels=False)
                        )

                        trace = problem.plot_function_solution(clicked_solution)



                        fig = go.Figure(layout=layout1)
                        if problem.plot_layout is not None:
                            fig.update_layout(
                                problem.plot_layout
                            )

                        # add the background dash_app if given as input.
                        # This could be the extent of the study area
                        if problem.plot_background_trace is not None:
                            fig.add_trace(problem.plot_background_trace)

                        fig.add_trace(trace)
                        #fig.update_layout(height=700, width=800)
                        return fig
                #if element is not found directly (mouse slightly off) prevent error message
                except  KeyError as error:
                    #raise PreventUpdate
                    pass
            return {}

    # Initialize dash app
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp3/',
        external_stylesheets=[
            "/static/stylesheets/style.css",
            "https://fonts.googleapis.com/css2?family=Bodoni+Moda&display=swap",
        ],
    )
    #dash_app.title = "Interactive paretofront"

    dash_app.layout = create_layout()

    ## Main function start
    filename = 'pareto_front.pkl'

    with open(os.path.join("data", filename), 'rb') as output:
        pf_comola = pickle.load(output)

    optimal_solutions_comola = []
    for i in range(len(pf_comola[2])):
        optimal_solutions_comola.append(Solution( np.array(pf_comola[2][i].representation),np.array(pf_comola[2][i].fitness).reshape((4,1))))

    comola_problem = Problem(
        name = "Fire treatment allocation",
        description = "none",
        nr_objectives= 1,
        benchmarks = [optimal_solutions_comola],
        objective_names = ["Maximize Crop Yield", "Maximize Habitat Heterogeneity", "Maximize Forest Species Richness", "Maximize Water Yield"],
        objective_descriptions = [
            "Crop yield basis on number of allocated land of cropland 1-5, where 1 has the lowest intensity and 5 the highest.",
            "Habitat Heterogeneity is computed by summing up the edges of neighboring cells with different land uses and assigning them a weight.",
            "Forest Species richness depends on the total area of forest.",
            "Each land use gets assigned a specific water yield parameter, and Crop land 1 is the optimal land use for this objective."
                ],
        objective_functions = [None, None],
        constraint_descriptions = ["Land use transition constraints: Urban can not be transitioned into another land use. Pasture can only be transitioned into Forest, not the other way.",
                                "Area constraints: Pasture has area constraints of minimum of 10% and maximum of 30% of the total area. Forest has area constraints of minimum of 10% and maximum of 25% of the total area."],
        validation_functions = [None],
        mathematical_formulation = None,
        plot_layout = None,
        plot_function_solution = plot_selected_landuse_map,
        plot_background_trace = None,
        plot_geographical_center = None,
        plot_function_additional_trace= None)

    problem = comola_problem

    interactiveParetoFront(dash_app, problem)
    ## Main function end

    return dash_app.server


