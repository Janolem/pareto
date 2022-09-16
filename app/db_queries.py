import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
#engine = create_engine('sqlite:///:memory:', echo=True)
#Session = sessionmaker(bind=engine)
#Base = declarative_base()
from app import db
from flask import Flask
from app.models import Problem, Solution, Variation, Constraint, Objective

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app


application = create_app()
application.app_context().push()
with application.app_context():
    db.create_all()
import sqlalchemy_utils
import os
basedir = r"C:\Users\morit\PycharmProjects\pareto"
#sqlalchemy_utils.functions.drop_database('sqlite:///' + os.path.join(basedir, 'app.db'))
create_engine('sqlite:///' + os.path.join(basedir, 'app.db'))

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

problems = Problem.query.all()
for p in problems:
    print(p.name)
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

# # id, name, description, function, mathematical_formulation
#
objective_1 = Objective(name="Soil Loss",
                        description="The empirical-based Revised Universal Soil Loss Equation (RUSLE)"
                                    "(Renard,1997) is used to estimate the soil loss of protected and unprotected "
                                    "sub-watersheds.",
                        mathematical_formulation=r"A = R \cdot K \cdot L \cdot S \cdot C \cdot P"
                        ,
                        symbols=r"A = \text{the estimated average annual soil loss and temporal average soil loss per unit of area in} t ha^{-1} yr^{-1}, "
                                r"R = \text{Rainfall-runoff erosivity factor in} MJ mm ha^{-1} h^{-1} yr^{-1}, "
                                r"L = Slope length factor in m, Slope steepness factor in radians,"
                                r"S = Slope steepness factor in radians, "
                                r"C = Cover management factor (unitless), "
                                r"P = Support practice factor (unitless). "
                        )

objective_2 = Objective(name="Labor Requirements",
                        description="We use empirical values of the labor requirements (Table 1) measured in" \
                                    "person days from Tenge et al (2005) for different slopes and soil types. The soil" \
                                    "types are categorized into stable and unstable soil, where clay soil is considered" \
                                    "stable and loam and sand are considered unstable (Tenge et al, 2005). Soil is" \
                                    "classified as clayey soil if the clay content is above 40%, or if the clay content" \
                                    "is above 35% as long as the sand content is below 45% (Garc ́ıa-Gaines and" \
                                    "Frankenstein, 2015). The labor requirement map is computed with slope, clay" \
                                    "and sand content raster",
                        mathematical_formulation=r"LD_{total} =A \sum_{n=1}^N ld_{n} "
                        , symbols=r"LD_{total} = Total labor days," \
                                  "n  = Current cell of labor requirement raster, " \
                                  "N  = Number of cells where SWC-measures are applied, " \
                                  "A = Cell size in ha, " \
                                  "ld_{n} = labor days per ha."
                        )
db.session.commit()
[variation_Gumobila.variation_has_objectives.append(o) for o in
 [objective_1, objective_2]]
db.session.commit()
[variation_Enerata.variation_has_objectives.append(o) for o in
 [objective_1, objective_2]]
db.session.commit()
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



comola = Problem(name='CoMOLA', description = "CoMOLA is a multi-objective constrained land use allocation problem. \
                                              It was formulated by Strauch et al. 2019 with multiple strengths of land use area and land use transition constraints.")

db.session.add(comola)
db.session.commit()

problems = Problem.query.all()
for p in Problem.query.filter_by(name='CoMOLA'):
    p_id = p.id


#class variation:     id, name, research_link, problem_id
variation_strong_constraints = Variation(name = "Strong constraints", research_link = r"https://www.sciencedirect.com/science/article/pii/S1364815218311204?via%3Dihub", problem_id = p_id)

#id, name, description, function, mathematical_formulation
constraint_1 = Constraint(name = "Forest area constraint >=10%",
                          description = "The land use forest must cover at least 10% of the total area",
                          mathematical_formulation = r"A_{Forest} >= \frac{A_{Total},10}")

constraint_2 = Constraint(name = "Forest area constraint <=25%",
                          description = "The land use Forest must cover less than or equal to 25% of the total area",
                          mathematical_formulation = r"A_{Forest} <= \frac{A_{Total},25}")

constraint_3 = Constraint(name = "Pasture area constraint >=10%",
                          description = "The land use Forest must cover at least 10% of the total area",
                          mathematical_formulation = r"A_{Pasture} >= \frac{A_{Total},10}")

constraint_4 = Constraint(name = "Pasture area constraint <=30%",
                          description = "The land use Pasture must cover less than or equal to 30% of the total area",
                          mathematical_formulation = r"A_{Pasture} <= \frac{A_{Total},30}")

constraint_5 = Constraint(name = "Forest transition constraint",
                          description = "Land use Forest can only transitioned into Pasture",
                          mathematical_formulation = "I_{Forest} = X_{Forest, Pasture}")

constraint_6 = Constraint(name = "Pasture transition constraint",
                          description = "Land use Pasture can not be transitioned into any other land use",
                          mathematical_formulation = "I_{Pasture} = X_{Pasture}")

constraint_7 = Constraint(name = "Urban transition constraint",
                          description = "Land use Urban can not be transitioned into any other land use",
                          mathematical_formulation = "I_{Urban} = X_{Urban}")

[variation_strong_constraints.variation_has_constraints.append(c) for c in [constraint_1, constraint_2, constraint_3, constraint_4, constraint_5, constraint_6, constraint_7]]

db.session.add(variation_strong_constraints)
db.session.commit()
cnstrnts = Constraint.query.join(Variation.variation_has_constraints).filter(Variation.variation_has_constraints.any(id=Variation.id))

for row in cnstrnts:
    print (row.id, row.name)

objective_1 = Objective(name = "Crop Yield",
                          description = "Crop yield (CY) is the sum of all logarithmic products of cropland intensity and soil fertility over all cells. It is the only objective function for which a second spatial input data set is required; a soil fertility map with values ranging from 0.1 to 1. The optimal valid solution for this objective is found when all permitted land use is transitioned into cropland 5 on the cells with the highest soil fertility value while the transition constraints are not violated. The worst solution has no cropland at all.",
                          mathematical_formulation = r"CY = \sum_{i=1}^{I} CY{i} = log(P_{i}(1+F_{i}))"
                          ,symbols = "$P_{i}$ = crop production intensity, F = soil fertility)"
                        )

objective_2 = Objective(name = "Species Richness",
                          description = "The species richness (SR) objective function bases on empirical relationships between habitat area and species richness from \citet{MacArthur.1967}. The number of grid cells of land use forest defines the objective value, and the objective value is the sum of 5 times the forest area to the power of 0.2. An optimal valid solution for this objective is a map where the maximum area constraint of forest is reached, the worst solution has the minimum permitted area of forest.",
                          mathematical_formulation = r"SR = 5 * A_{F} ^{0.2}"
                          ,symbols = "$A_{F}$ = area of forest"
                        )

objective_3 = Objective(name = "Habitat Heterogeneity",
                          description = "The habitat heterogeneity (HH) is the sum over edges between different land use types, i.e. between patches. Edges have different weights: a higher land use intensity leads to a lower habitat heterogeneity. Edges with forest, pasture and cropland 1 have the lowest intensity and get a weight of 1, edges with cropland 2-5 have corresponding intensity weights of 2-5. Edges with urban are ignored and therefore do not contribute to a higher habitat heterogeneity. The optimal valid solution for this objective has the highest possible number of edges between forest, pasture and cropland 1 obtainable under the maximum area constraints of 25\% forest and 30\% pasture. The worst solution has minimum forest area, minimum pasture area and urban or cropland 5 for the remaining cells areas.",
                          mathematical_formulation = r"HH = \sum_{i=1}^{5} HH_{E_{i}} = \frac{E_{I}}{I}"
                        ,symbols = "E = number of edges, I = edge intensity"
                        )

objective_4 = Objective(name = "Water Yield",
                          description = "The water yield (WY) objective function is based on the relative differences in evapotranspiration rates between land use types. The total water yield is computed by summing all land use areas divided by the the land-use specific evapotranspiration rate. The evapotranspiration rates are, in increasing order: cropland 1 = 0.900, cropland 2 = 0.925, cropland 3 = 0.950, pasture = 0.960, cropland 4 = 0.975, cropland 5 = 1.00, forest = 1.14. The optimal valid solution for this objective is found when the minimum area constraint of forest and pasture are reached and the other remaining study area is cropland 1. The worst solution is composed by maximum allowed forest area, maximum allowed pasture area and cropland 5 for the remaining areas.",
                          mathematical_formulation = r"WY = \sum_{c=1}^{7} WY_{A_{c}} = \frac{A_{Kc}}{K_{c}}",
                          symbols = "Kc = evaporation rate, $A_{Kc}$ = area of land use with evatransporation rate $K_{c}$")
db.session.commit()
[variation_strong_constraints.variation_has_objectives.append(o) for o in [objective_1, objective_2, objective_3, objective_4]]
db.session.commit()
objs = Objective.query.join(Variation.variation_has_objectives).filter(Variation.variation_has_objectives.any(id=Objective.id))
for row in objs:
    print (row.id, row.name)

string_mathematical_formulation = ""
string_mathematical_formulation = [ string_mathematical_formulation + o.mathematical_formulation for o in objs] + [  string_mathematical_formulation + c.mathematical_formulation for c in cnstrnts]
string_mathematical_formulation = '\n'.join(string_mathematical_formulation)
print(string_mathematical_formulation)

variations = Variation.query.all()

for v in variations:
    print(v.id, v.name, v.research_link)

db.session.commit()


# problems2 = Problem.query.all()
# for p in problems2:
#     db.session.delete(p)
#
# variations2 = Variation.query.all()
# for v in variations2:
#     db.session.delete(v)
#
# constraints2 = Constraint.query.all()
# for c in constraints2:
#     db.session.delete(c)
#
# objectives2 = Objective.query.all()
# for o in objectives2:
#     db.session.delete(o)
#
# db.session.commit()
