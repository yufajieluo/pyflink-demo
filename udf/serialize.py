import json
from pyflink.table import DataTypes
from pyflink.table.udf import udf, ScalarFunction

class Get(ScalarFunction):
    def eval(self, line, key):
        try:
            json_line = json.loads(line)
            json_line['serialize'] = True
        except:
            json_line = {'serialize': False}
        return str(json_line.get(key))

get = udf(
    Get(),
    [ DataTypes.STRING(), DataTypes.STRING() ],
    DataTypes.STRING()
)