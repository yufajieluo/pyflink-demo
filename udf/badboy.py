from pyflink.table import DataTypes
from pyflink.table.udf import udf, ScalarFunction

class Badboy(ScalarFunction):

    def eval(self, wife):
        result = None
        if wife != 'dxj':
            result = False
        else:
            result = True
        return result

badboy = udf(
    Badboy(), 
    [ DataTypes.STRING() ], 
    DataTypes.BOOLEAN()
)