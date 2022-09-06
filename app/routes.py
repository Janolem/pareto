"""Routes for parent Flask app."""
from flask import render_template, url_for, current_app as app
from flask_babel import _, get_locale
from app.models import Problem, Solution, Variation, Constraint, Objective
from flask import Flask
import json

@app.route('/')
@app.route('/home')
def home():
    """Landing page."""
    return render_template(
        'home.html',
        title=_('Home')
    )

@app.route('/explore')
def explore():
    """Explore page."""
    return render_template(
        'explore.html',
        title=_('Explore')
    )

@app.route('/pareto1')
def pareto1():
    """pareto front1"""
    from app import db
    with app.app_context():
        db.create_all()

    problems2 = Problem.query.all()
    for p in problems2:
        db.session.delete(p)

    variations2 = Variation.query.all()
    for v in variations2:
        db.session.delete(v)

    constraints2 = Constraint.query.all()
    for c in constraints2:
        db.session.delete(c)

    objectives2 = Objective.query.all()
    for o in objectives2:
        db.session.delete(o)

    db.session.commit()
    #
    #
    # # if db is empty execute the following code with the db inserts

    swc = Problem(name='SWC allocation optimization',
                     description="The Soil and Water Conservation Measure Allocation problem is a "\
                                 "study conducted to find optimal allocations of installing the labor "\
                                 "intensive SWC measure bench terraces in Ethiopia. Three study areas were used: "\
                                 "Kebele Gumobila, Kebele Enerata and Kebele Mender 51."\
                                 "The study areas are affected by high soil loss rates and is known " \
                                 "to suffer from the soil losses. Gumobila located in the north-western part of Ethiopia" \
                                 "and it belongs to the West Gojjam zone in the Amhara region. " \
                                 "The altitude of Gumobila ranges from 2048 m to 3106 m above zero with a mean annual " \
                                 "rainfall of 1970 mm and is situated in the agro-ecological zone Wet Dega. " \
                                 "The second study area Enerata hasan altitude between 2283 m and 2638 m above "\
                                 "zero and mean annual rainfallof 1305 mm and is situated in the agro-ecological "\
                                 "zone called Moist Dega. The most western study area Kebele Mender 51 is classified "\
                                 "as Wet Kolla with an altitude between 1335 m and 1478 m above zero and a "\
                                 "mean annual rainfall of 1780 mm.")

    db.session.add(swc)
    db.session.commit()
    #
    for p in Problem.query.filter_by(name='SWC allocation optimization'):
        p_id = p.id
        print(p.name)

    # class variation:     id, name, research_link, problem_id
    variation_Gumobila = Variation(name="Gumobila",
                                    research_link=r"https://www.researchsquare.com/article/rs-1735209/v1",
                                    problem_id=p_id)
    variation_Enerata = Variation(name="Enerata",
                                    research_link=r"https://www.researchsquare.com/article/rs-1735209/v1",
                                    problem_id=p_id)
    variation_Mender51 = Variation(name="Mender51",
                                    research_link=r"https://www.researchsquare.com/article/rs-1735209/v1",
                                    problem_id=p_id)

    constraint = Constraint(name="No constraints",
                              description="This optimization variation has no defined constraints",
                              mathematical_formulation=r" "
                              ,symbols = r" ")

    #variation_Gumobila.variation_has_constraints.append(constraint)
    #variation_Enerata.variation_has_constraints.append(constraint)
    #variation_Mender51.variation_has_constraints.append(constraint)

    db.session.add(variation_Gumobila)
    db.session.add(variation_Enerata)
    db.session.add(variation_Mender51)
    db.session.commit()

    # # id, name, description, function, mathematical_formulation
    #
    objective_1 = Objective(name="Soil Loss",
                            description="""The empirical-based Revised Universal Soil Loss Equation (RUSLE)
                                        (Renard,1997) is used to estimate the soil loss of protected and unprotected
                                        sub-watersheds.""",
                            mathematical_formulation=r"A = R \cdot K \cdot L \cdot S \cdot C \cdot P"
                            , symbols=r"""A = \text{the estimated average annual soil loss and temporal average soil loss per unit of area in } t\;ha^{-1}\;yr^{-1}, 
                                      R = \text{Rainfall-runoff erosivity factor in } MJ\;mm\;ha^{-1}\;h^{-1}\;yr^{-1}, 
                                      L = \text{Slope length factor in m, Slope steepness factor in radians}, 
                                      S = \text{Slope steepness factor in radians}, 
                                      C = \text{Cover management factor (unitless)}, 
                                      P = \text{Support practice factor (unitless).} """
                            )

    objective_2 = Objective(name="Labor Requirements",
                            description= r"""We use empirical values of the labor requirements (Table 1) measured in
                            person days from Tenge et al (2005) for different slopes and soil types. The soil
                            types are categorized into stable and unstable soil, where clay soil is considered
                            stable and loam and sand are considered unstable (Tenge et al, 2005). Soil is
                            classified as clayey soil if the clay content is above 40%, or if the clay content
                            is above 35% as long as the sand content is below 45% (Garc ́ıa-Gaines and
                            Frankenstein, 2015). The labor requirement map is computed with slope, clay
                            and sand content raster """,
                            mathematical_formulation=r"LD_{total} =A \sum_{n=1}^N ld_{n} "
                            , symbols=r"LD_{total} = \text{Total labor days},"\
                                r"n  = \text{Current cell of labor requirement raster}, "\
                                r"N  = \text{Number of cells where SWC-measures are applied}, "\
                                r"A = \text{Cell size in ha}, " \
                                 r"ld_{n} = \text{labor days per ha.}"
                            )
    db.session.commit()
    [variation_Gumobila.variation_has_objectives.append(o) for o in
    [objective_1, objective_2]]
    [variation_Enerata.variation_has_objectives.append(o) for o in
    [objective_1, objective_2]]
    [variation_Mender51.variation_has_objectives.append(o) for o in
    [objective_1, objective_2]]

    db.session.commit()

    for p in Problem.query.filter_by(name='SWC allocation optimization'):
        p_id = p.id
        problem_name = p.name
        problem_description = p.description

    objectives = Objective.query.join(Variation.variation_has_objectives).filter(
        Variation.variation_has_objectives.any(id=Objective.id))

    for row in objectives:
        print(row.id, row.name)

    constraints = Constraint.query.join(Variation.variation_has_constraints).filter(
        Variation.variation_has_constraints.any(id=Variation.id))
    string_mathematical_formulation = ""
    string_mathematical_formulation = [string_mathematical_formulation + o.mathematical_formulation for o in
                                       objectives] + [string_mathematical_formulation + c.mathematical_formulation for c
                                                      in constraints]
    print(string_mathematical_formulation)
    string_mathematical_formulation = '\n'.join(string_mathematical_formulation)
    return render_template(
        'pareto1.html',
        title=_(problem_name),
        problem_description=problem_description,
        objectives=[row for row in objectives],
        constraints=[row for row in constraints],
    )

@app.route('/pareto2')
def pareto2():
    """pareto front2"""
    from app import db
    with app.app_context():
        db.create_all()

    problems2 = Problem.query.all()
    for p in problems2:
        db.session.delete(p)

    variations2 = Variation.query.all()
    for v in variations2:
        db.session.delete(v)

    constraints2 = Constraint.query.all()
    for c in constraints2:
        db.session.delete(c)

    objectives2 = Objective.query.all()
    for o in objectives2:
        db.session.delete(o)

    db.session.commit()


    # if db is empty execute the following code with the db inserts
    comola = Problem(name='CoMOLA', description="CoMOLA is a multi-objective constrained land use allocation problem. \
                                                  It was formulated by Strauch et al. 2019 with multiple strengths of land use area and land use transition constraints.")

    db.session.add(comola)
    db.session.commit()
    #
    problems = Problem.query.all()
    for p in Problem.query.filter_by(name='CoMOLA'):
        p_id = p.id

    # class variation:     id, name, research_link, problem_id
    variation_strong_constraints = Variation(name="Strong constraints",
                                             research_link=r"https://www.sciencedirect.com/science/article/pii/S1364815218311204?via%3Dihub",
                                             problem_id=p_id)

    # id, name, description, function, mathematical_formulation
    constraint_1 = Constraint(name="Forest area constraint >=10%",
                              description="The land use forest must cover at least 10% of the total area",
                              mathematical_formulation=r"A_{Forest} >= \frac{A_{Total}}{10}"
                              ,symbols = r"A_{Forest} = \text{Area of land use forest}, A_{Total} = \text{Total Area}")

    constraint_2 = Constraint(name="Forest area constraint <=25%",
                              description="The land use Forest must cover less than or equal to 25% of the total area",
                              mathematical_formulation=r"A_{Forest} <= \frac{A_{Total}}{25}"
                              ,symbols = r"A_{Forest} = \text{Area of land use forest}, A_{Total} = \text{Total Area}")

    constraint_3 = Constraint(name="Pasture area constraint >=10%",
                              description="The land use Forest must cover at least 10% of the total area",
                              mathematical_formulation=r"A_{Pasture} >= \frac{A_{Total}}{10}"
                              ,symbols = r"A_{Pasture} = \text{Area of land use pasture}, A_{Total} = \text{Total Area}")

    constraint_4 = Constraint(name="Pasture area constraint <=30%",
                              description="The land use Pasture must cover less than or equal to 30% of the total area",
                              mathematical_formulation=r"A_{Pasture} <= \frac{A_{Total}}{30}"
                              , symbols=r"A_{Pasture} = \text{Area of land use pasture}, A_{Total} = \text{Total Area}")

    constraint_5 = Constraint(name="Forest transition constraint",
                              description="Land use Forest can only be transitioned into Pasture",
                              mathematical_formulation="I_{Forest} = X_{Forest, Pasture}"
                              , symbols=r"I_{Forest} = \text{Initial land use of type forest}, X_{Forest, Pasture} = \text{Decision variable of type forest or pasture}")

    constraint_6 = Constraint(name="Pasture transition constraint",
                              description="Land use Pasture can not be transitioned into any other land use",
                              mathematical_formulation="I_{Pasture} = X_{Pasture}"
                            , symbols = r"I_{Pasture} = \text{Initial land use of type pasture}, X_{Pasture} = \text{Decision variable of type pasture}")


    constraint_7 = Constraint(name="Urban transition constraint",
                              description="Land use Urban can not be transitioned into any other land use",
                              mathematical_formulation="I_{Urban} = X_{Urban}"
                              ,symbols=r"I_{Urban} = \text{Initial land use of type pasture}, X_{Pasture} = \text{Decision variable of type urban}")

    [variation_strong_constraints.variation_has_constraints.append(c) for c in
     [constraint_1, constraint_2, constraint_3, constraint_4, constraint_5, constraint_6, constraint_7]]

    db.session.add(variation_strong_constraints)
    db.session.commit()
    cnstrnts = Constraint.query.join(Variation.variation_has_constraints).filter(
        Variation.variation_has_constraints.any(id=Variation.id))

    for row in cnstrnts:
        print(row.id, row.name)

    objective_1 = Objective(name="Crop Yield",
                            description="Crop yield (CY) is the sum of all logarithmic products of cropland intensity and soil fertility over all cells. It is the only objective function for which a second spatial input data set is required; a soil fertility map with values ranging from 0.1 to 1. The optimal valid solution for this objective is found when all permitted land use is transitioned into cropland 5 on the cells with the highest soil fertility value while the transition constraints are not violated. The worst solution has no cropland at all.",
                            mathematical_formulation=r"CY = \sum_{i=1}^{I} CY{i} = log(P_{i}(1+F_{i}))"
                            , symbols=r"P_{i} = \text{Crop production intensity}, F = \text{Soil fertility}"
                            )

    objective_2 = Objective(name="Species Richness",
                            description="The species richness (SR) objective function bases on empirical relationships between habitat area and species richness from \citet{MacArthur.1967}. The number of grid cells of land use forest defines the objective value, and the objective value is the sum of 5 times the forest area to the power of 0.2. An optimal valid solution for this objective is a map where the maximum area constraint of forest is reached, the worst solution has the minimum permitted area of forest.",
                            mathematical_formulation=r"SR = 5 * A_{F} ^{0.2}"
                            , symbols=r"A_{F} = \text{Area of land use forest}"
                            )

    objective_3 = Objective(name="Habitat Heterogeneity",
                            description="The habitat heterogeneity (HH) is the sum over edges between different land use types, i.e. between patches. Edges have different weights: a higher land use intensity leads to a lower habitat heterogeneity. Edges with forest, pasture and cropland 1 have the lowest intensity and get a weight of 1, edges with cropland 2-5 have corresponding intensity weights of 2-5. Edges with urban are ignored and therefore do not contribute to a higher habitat heterogeneity. The optimal valid solution for this objective has the highest possible number of edges between forest, pasture and cropland 1 obtainable under the maximum area constraints of 25\% forest and 30\% pasture. The worst solution has minimum forest area, minimum pasture area and urban or cropland 5 for the remaining cells areas.",
                            mathematical_formulation=r"HH = \sum_{i=1}^{5} HH_{E_{i}} = \frac{E_{I}}{I}"
                            , symbols=r"E = \text{Number of edges}, I = \text{Edge intensity}"
                            )

    objective_4 = Objective(name="Water Yield",
                            description="The water yield (WY) objective function is based on the relative differences in evapotranspiration rates between land use types. The total water yield is computed by summing all land use areas divided by the the land-use specific evapotranspiration rate. The evapotranspiration rates are, in increasing order: cropland 1 = 0.900, cropland 2 = 0.925, cropland 3 = 0.950, pasture = 0.960, cropland 4 = 0.975, cropland 5 = 1.00, forest = 1.14. The optimal valid solution for this objective is found when the minimum area constraint of forest and pasture are reached and the other remaining study area is cropland 1. The worst solution is composed by maximum allowed forest area, maximum allowed pasture area and cropland 5 for the remaining areas.",
                            mathematical_formulation=r"WY = \sum_{c=1}^{7} WY_{A_{c}} = \frac{A_{Kc}}{K_{c}}",
                            symbols=r"Kc = \text{Evaporation rate,} A_{Kc} = \text{Area of land use with evatransporation rate} K_{c}")
    db.session.commit()
    [variation_strong_constraints.variation_has_objectives.append(o) for o in
    [objective_1, objective_2, objective_3, objective_4]]

    db.session.commit()

    for p in Problem.query.filter_by(name='CoMOLA'):
        p_id = p.id
        problem_name = p.name
        problem_description = p.description

    objectives = Objective.query.join(Variation.variation_has_objectives).filter(
        Variation.variation_has_objectives.any(id=Objective.id))
    for row in objectives:
        print(row.id, row.name)
    constraints = Constraint.query.join(Variation.variation_has_constraints).filter(
        Variation.variation_has_constraints.any(id=Variation.id))
    string_mathematical_formulation = ""
    string_mathematical_formulation = [string_mathematical_formulation + o.mathematical_formulation for o in
                                       objectives] + [string_mathematical_formulation + c.mathematical_formulation for c
                                                      in constraints]
    print(string_mathematical_formulation)
    string_mathematical_formulation = '\n'.join(string_mathematical_formulation)
    return render_template(
        'pareto2.html',
        title=_(problem_name),
        problem_description=problem_description,
        objectives=[row for row in objectives],
        constraints=[row for row in constraints],
    )

@app.route('/pareto3')
def pareto3():
    """pareto front2"""
    from app import db

    with app.app_context():
        db.create_all()

    problems2 = Problem.query.all()
    for p in problems2:
        db.session.delete(p)

    variations2 = Variation.query.all()
    for v in variations2:
        db.session.delete(v)

    constraints2 = Constraint.query.all()
    for c in constraints2:
        db.session.delete(c)

    objectives2 = Objective.query.all()
    for o in objectives2:
        db.session.delete(o)

    db.session.commit()


    # if db is empty execute the following code with the db inserts
    lmu57 = Problem(name='Forest treatment optimization',
                     description="""Optimally allocated fuel reduction treatments can be sufficient to reduce the
                            wild fire risk of the landscape, Finney (2001) showed that treating about 25%
                            of the total landscape can be enough to reduce the fire spread rate and inten-
                            sity. The goal for this problem is to find 
                            the optimal units for forest treatment with a defined area treatment treshold.""")

    db.session.add(lmu57)
    db.session.commit()

    for p in Problem.query.filter_by(name='Forest treatment optimization'):
        p_id = p.id
        problem_name = p.name
        problem_description = p.description

    # class variation:     id, name, research_link, problem_id
    variation_StanislausLMU57 = Variation(name="StanislausLMU57",
                                             research_link=r"https://scholarspace.manoa.hawaii.edu/items/88176290-6ab2-4146-b19d-1c09191f5458",
                                             problem_id=p_id)

    # id, name, description, function, mathematical_formulation
    constraint_1 = Constraint(name="Treshold",
                              description="The treshold constraint defines the maximum area for forest treatments.",
                              mathematical_formulation=r"\sum_{i} \alpha_{i} X_{i} \leq T"
                              ,symbols = r"i = \text{Index of land management units}, "\
                                         r"\alpha_{i} = \text{the area of unit} i, "\
                                         r"T = \text{the threshold on the treated project area}")

    constraint_2 = Constraint(name="Contiguity constraint linear equation 1",
                              description=r"Part one of the contiguity constraint formulation with a connected fluid network representation"\
                                          r" after Shirabe (2005).",
                              mathematical_formulation=r"\sum_{j \in N_{i}} Y_{ij} - \sum_{j \in N_{i}} Y_{ji} \geq X_{i} - M V_{i} \; \forall i \\"
                              ,symbols = r"N_{i} = \text{Spatial neighbors of unit $i$ (here based on adjacency)}, "
                                         r"Y_{ij} = \text{Decision variable indicating flow between units }i \text{and }j,"
                                         r"M = \text{Number of treatment areas},"
                                         r"X_{i} = \text{The decision variable indicating treatment (}X_{i}\text{ = 1) or no treatment (}X_{i}\text{ = 0) for unit }X_{i}")


    constraint_3 = Constraint(name="Contiguity constraint linear equation 2",
                              description=r"Part two of the contiguity constraint formulation with a connected fluid network representation"\
                                          r" after Shirabe (2005). Defines that decision variable can only take the values 0 or 1. ",
                              mathematical_formulation=r"X_{i} = {0,1} \; \forall i "
                              ,symbols = r"V_{i} = \text{The decision variable indicating whether or not unit $i$ is a sink.}")

    constraint_4 = Constraint(name="Contiguity constraint linear equation 3",
                              description=r"Part three of the contiguity constraint formulation with a connected fluid network representation"\
                                          r" after Shirabe (2005). Defines that there can only be one sink.",
                              mathematical_formulation=r"\sum_{i} V_{i} = 1"
                              , symbols=r"i = \text{Index of land management units,}"
                                        r"V_{i} = \text{The decision variable indicating whether or not unit $i$ is a sink.}")

    constraint_5 = Constraint(name="Contiguity constraint linear equation 4",
                              description=r"Part four of the contiguity constraint formulation with a connected fluid network representation"\
                                          r" after Shirabe (2005). Defines whether a unit is a sink (1) or not (0)",
                              mathematical_formulation=r"V_{i} = {0,1} \; \forall i"
                              , symbols=r"i = \text{Index of land management units,}"
                                        r"V_{i} = \text{The decision variable indicating whether or not unit $i$ is a sink.}")

    constraint_6 = Constraint(name="Contiguity constraint linear equation 5",
                              description= r"Part five of the contiguity constraint formulation with a connected fluid network representation"\
                                          r" after Shirabe (2005). Defines that the flow can not be negative between units.",
                              mathematical_formulation=r"Y_{ij} \geq 0 \; \forall i,j"
                              , symbols=r"Y_{ij} = \text{Decision variable indicating flow between units }i \text{and }j.")

    [variation_StanislausLMU57.variation_has_constraints.append(c) for c in
     [constraint_1, constraint_2, constraint_3, constraint_4, constraint_5, constraint_6]]

    db.session.add(variation_StanislausLMU57)
    db.session.commit()
    cnstrnts = Constraint.query.join(Variation.variation_has_constraints).filter(
        Variation.variation_has_constraints.any(id=Variation.id))

    objective_1 = Objective(name="Departure from historical conditions",
                            description="The objective is to maximize the benefit; and the benefit increases with decreasing "
                                        "departure from historical conditions. For every forest management unit, "
                                        "the departure variable is knowm by comparing the Historical Range and Variability "
                                        "to current forest conditions. The reasoning behind this objective is the much higher forest "
                                        "fire resilience of the past.",
                            mathematical_formulation=r"Maximize \sum_{i} \beta_{i} X_{i}"
                            , symbols=r"i = \text{Index of land management units}, \beta_{i} = \text{benefit of treating unit}, X_{i} = \text{the decision variable indicating treatment (}X_{i} = 1\text{) or no treatment (}X_{i} = 0\text{) for unit} X_{i}"
                            )

    db.session.commit()
    variation_StanislausLMU57.variation_has_objectives.append(objective_1)

    db.session.commit()

    objectives = Objective.query.join(Variation.variation_has_objectives).filter(
        Variation.variation_has_objectives.any(id=Objective.id))
    for row in objectives:
        print(row.id, row.name)
    constraints = Constraint.query.join(Variation.variation_has_constraints).filter(
        Variation.variation_has_constraints.any(id=Variation.id))
    string_mathematical_formulation = ""
    string_mathematical_formulation = [string_mathematical_formulation + o.mathematical_formulation for o in
                                       objectives] + [string_mathematical_formulation + c.mathematical_formulation for c
                                                      in constraints]
    print(string_mathematical_formulation)
    string_mathematical_formulation = '\n'.join(string_mathematical_formulation)
    return render_template(
        'pareto3.html',
        title=_(problem_name),
        problem_description=problem_description,
        objectives=[row for row in objectives],
        constraints=[row for row in constraints],
    )