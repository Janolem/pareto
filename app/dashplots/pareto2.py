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

from flask import Flask
from app import db
from app.models import Problem, Solution, Variation, Constraint, Objective

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app

application = create_app()
application.app_context().push()
with application.app_context():
    db.create_all()

def init_pareto2(server):

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
                                            id="pareto_front", style={"display": "inline-block" , "height": "50vh", "width": "40vh"}
                                        ),
                                        dcc.Graph(
                                            id="selected_data", style={"display": "inline-block" , "height": "50vh", "width": "40vh"}
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

            # figure.update_layout(
            #     title={
            #         'y': 0.975,
            #         'x': 0.055,
            #         'xanchor': 'left',
            #         'yanchor': 'top'},
            #     legend={'itemsizing': 'constant'})

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
        routes_pathname_prefix='/dashapp2/',
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

    p = Problem.query.filter_by(name='CoMOLA').fetchone()
    objectives = Objective.query.join(Variation.variation_has_objectives).filter(
        Variation.variation_has_objectives.any(id=Objective.id))
    constraints = Constraint.query.join(Variation.variation_has_constraints).filter(Variation.variation_has_constraints.any(id=Variation.id))
    string_mathematical_formulation = ""
    string_mathematical_formulation = [ string_mathematical_formulation + o.mathematical_formulation for o in objectives] + [  string_mathematical_formulation + c.mathematical_formulation for c in constraints]
    string_mathematical_formulation = '\n'.join(string_mathematical_formulation)


    comola_problem = Problem(
        name = p.name,
        description = p.description,
        nr_objectives= 4,
        benchmarks = [optimal_solutions_comola],
        objective_names = [o.name for o in objectives],
        objective_descriptions = [o.description for o in objectives],
        objective_functions = [None, None],
        constraint_descriptions = [c.description for c in constraints],
        validation_functions = [None],
        mathematical_formulation = string_mathematical_formulation,
        plot_layout = None,
        plot_function_solution = plot_selected_landuse_map,
        plot_background_trace = None,
        plot_geographical_center = None,
        plot_function_additional_trace= None)

    problem = comola_problem

    interactiveParetoFront(dash_app, problem)
    ## Main function end

    return dash_app.server


