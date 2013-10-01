__all__ = ['Direct']

import os, sys, copy
import numpy as np

from openmdao.main.api import Component, Variable
from openmdao.main.datatypes.api import Array
from openmdao.main.datatypes.file import File, FileRef

from SU2.io import Config, State
from SU2.run import direct, deform, adjoint

# ------------------------------------------------------------
#  Setup
# ------------------------------------------------------------

SU2_RUN = os.environ['SU2_RUN'] 
sys.path.append( SU2_RUN )

# SU2 suite run command template
base_Command = os.path.join(SU2_RUN,'%s')

# check for slurm
slurm_job = os.environ.has_key('SLURM_JOBID')
    
# set mpi command
if slurm_job:
    mpi_Command = 'srun -n %i %s'
else:
    mpi_Command = 'mpirun -np %i %s'


class ConfigVar(Variable):
    def __init__(self, default_value=None, iotype=None, desc=None, 
                 **metadata):
        super(ConfigVar, self).__init__(default_value=default_value,
                                    	**metadata)

    def validate(self, obj, name, value):
        """ Validates that a specified value is valid for this trait.
        Units are converted as needed.
        """
        if not isinstance(value, Config):
        	raise TypeError("value of '%s' must be a Config object" % name)
        return value

def pts_from_mesh(meshfile, config):

    mesh = SU2.mesh.tools.read(meshfile)

    markers = config.MARKER_MONITORING
    markers = markers.strip().strip('()').strip()
    markers = ''.join(markers.split())
    markers = markers.split(',')

    _,nodes = SU2.mesh.tools.get_markerPoints(mesh,markers)

    return len(nodes)


# ------------------------------------------------------------
#  SU2 Suite Interface Functions
# ------------------------------------------------------------

class Deform(Component):

    config_in = ConfigVar(Config(), iotype='in')
    dv_vals = Array([], iotype='in')
    config_out = ConfigVar(Config(), iotype='out', copy='deep')

    def configure(self):
        meshfile = self.config.MESH_FILENAME
        # - read number of unique pts from mesh file
        npts = pts_from_mesh(meshfile)
        # - create mesh_file trait with data_shape attribute
        self.add('mesh_file', File(iotype='out', data_shape=(npts,1)))

    def execute(self):
	    # local copy
        state = deform(self.config_in)
        self.mesh_file = FileRef(path=state.FILES.MESH)
        self.config_out = self.config_in

    def linearize(self):
        self.config_in.SURFACE_ADJ_FILENAME = self.config_in.SURFACE_FLOW_FILENAME
        SU2.run.projection(self.config_in)
        # read Jacobian info from file


_obj_names = [
    "LIFT",
    "DRAG",
    "SIDEFORCE",
    "MOMENT_X",
    "MOMENT_Y",
    "MOMENT_Z",
    "FORCE_X",
    "FORCE_Y",
    "FORCE_Z"
]

class Solve(Component):

    config_in = ConfigVar(Config(), iotype='in')
    mesh_file = File(iotype='in')
    for name in _obj_names:
        setattr(Solve, name, Float(0.0, iotype='out'))

    def configure(self):
        pass

    def execute(self):
        # local copy
        state = direct(self.config_in)
        for name in _obj_names:
            setattr(self, name, state.FUNCTIONS[name])

    def linearize(self):
        for name in _obj_names:
            config_in.ADJ_OBJ_FUNC = name
            state = adjoint(self.config_in)
            csvname = self.config_in.SURFACE_ADJ_FILENAME+'.csv'
            suffix = SU2.io.tools.get_adjointSuffix(name)
            csvname = SU2.io.tools.add_suffix(csvname, suffix)
            # read a CSV file (graph first 2 cols (index, sensitivity), sort by index)
            # transpose


          
      
if __name__ == '__main__':
    pass