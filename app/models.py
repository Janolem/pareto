from sqlalchemy import PickleType
from app import db

__table_args__ = {'extend_existing': True}

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    description = db.Column(db.String)

    def __repr__(self):
        return '<Problem: {}>'.format(self.name)


class Plot_function(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name =  db.Column(db.String(120))
    type = db.Column(db.String(12)) # TODO: Check for constraint possibilies for type input in case that __table_args__ won't work
    minimum_nr_objectives = db.Column(db.Integer)
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id'))

    def __repr__(self):
        return '<Plot_function: {}>'.format(self.name)

    #__table_args__ = (CheckConstraint(type.in_(["background", "solution", "pareto"])))


variations_have_constraints = db.Table('Variations_have_constraints',
    db.Column('constraint_id', db.Integer, db.ForeignKey('constraint.id'), primary_key=True),
    db.Column('variation_id', db.Integer, db.ForeignKey('variation.id'), primary_key=True)
)

variations_have_objectives = db.Table('Variations_have_objectives',
    db.Column('objective_id', db.Integer, db.ForeignKey('objective.id'), primary_key=True),
    db.Column('variation_id', db.Integer, db.ForeignKey('variation.id'), primary_key=True)
)


class Variation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    research_link = db.Column(db.String)
    problem_id = db.Column(db.Integer, db.ForeignKey("problem.id"))
    variation_has_constraints = db.relationship('Constraint', secondary=variations_have_constraints, lazy='subquery', backref=db.backref('Variation', lazy=True))
    variation_has_objectives = db.relationship('Objective', secondary=variations_have_objectives, lazy='subquery', backref=db.backref('Variation', lazy=True))
    def __repr__(self):
        return '<Variation: {}>'.format(self.name)


class Constraint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    description = db.Column(db.String)
    mathematical_formulation = db.Column(db.String)
    symbols = db.Column(db.String)

    def __repr__(self):
        return '<Constraint: {}>'.format(self.name)


class Objective(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    description = db.Column(db.String)
    mathematical_formulation = db.Column(db.String)
    symbols = db.Column(db.String)

    def __repr__(self):
        return '<Objective: {}>'.format(self.name)
	

class Pareto_front(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    algorithm_description = db.Column(db.String)
    research_link = db.Column(db.String)
    variation_id = db.Column(db.Integer, db.ForeignKey("variation.id"))

    def __repr__(self):
        return '<Pareto_front: {}>'.format(self.name)
	
	
class Solution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    representation = db.Column(db.PickleType(), default = [])
    objective_values = db.Column(db.PickleType(), default = [])
    pareto_front_id = db.Column(db.Integer, db.ForeignKey("pareto_front.id"))

    def __repr__(self):
        return '<Solution: {}>'.format(self.name)