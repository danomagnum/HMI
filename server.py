#! /usr/bin/python

from flask import Flask, jsonify, send_from_directory, render_template, render_template_string, request
import jinja2
import json
import drivers
import inspect
#import thread
import threading
import time
import waitress

app = Flask(__name__)
TICKRATE = 0.1

sources = {}

class SilentUndefined(jinja2.Undefined):
  def _fail_with_undefined_error(self, *args, **kwargs):
    return "???"
  __add__ = __radd__ = __mul__ = __rmul__ = __div__ = __rdiv__ = \
__truediv__ = __rtruediv__ = __floordiv__ = __rfloordiv__ = \
__mod__ = __rmod__ = __pos__ = __neg__ = __call__ = \
__getitem__ = __lt__ = __le__ = __gt__ = __ge__ = __int__ = \
__float__ = __complex__ = __pow__ = __rpow__ = \
_fail_with_undefined_error   

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates/'), undefined=SilentUndefined)

@app.route('/read/<string:source>/<path:tag>')
def read_from_source(source, tag):
  if source in sources:
    return jsonify(sources[source].read(tag))
  else:
    return jsonify({'value':'Invalid Source' + source})


@app.route('/read_multi/', methods=['POST'])
def read_multi_from_source():
  #print(request.json)
  results = {}
  for path in request.json:
    source, tag = path.split('/')
    values = sources[source].read(tag)
    for key in values:
      results[f'{source}/{key}'] = values[key]
  res = jsonify(results)
  return res



@app.route('/write/<string:source>/<path:tag>', methods=['POST'])
def write_to_source(source, tag):
  print(request.form['value'])

  val = request.form['value']

  if source in sources:
    return jsonify(sources[source].write(tag, val))
  else:
    return jsonify({'value':'Invalid Source' + source})

@app.route('/')
def index():
  return send_from_directory('templates', 'main.html')

@app.route('/main.css')
def css():
  return send_from_directory('templates', 'main.css')

@app.route('/main.js')
def js():
  return send_from_directory('templates', 'main.js')


@app.route('/save/<string:screenid>', methods=['POST'])
def save_screen(screenid):
  #with open('screens/' + screenid + '.html', 'r') as myfile:
  # #data = myfile.read()
  #subtemplate = env.from_string(data)
  #subdata = subtemplate.render(**request.args)
  #subdata = render_template_string(data, undefined=SilentUndefined, **request.args)

  #return render_template('main.html', body=subdata, undefined=SilentUndefined, **request.args)
  data = request.form['content']

  with open('screens/' + screenid + '.html', 'w') as myfile:
      myfile.write(data)

  return render_template('edit.html', body=data, screenid=screenid, undefined=SilentUndefined, **request.args)

@app.route('/edit/<string:screenid>')
def edit_screen(screenid):
  with open('screens/' + screenid + '.html', 'r') as myfile:
    data = myfile.read()
  #subtemplate = env.from_string(data)
  #subdata = subtemplate.render(**request.args)
  #subdata = render_template_string(data, undefined=SilentUndefined, **request.args)

  #return render_template('main.html', body=subdata, undefined=SilentUndefined, **request.args)
  return render_template('edit.html', body=data, screenid=screenid, undefined=SilentUndefined, **request.args)



#todo: remove
@app.route('/screens/<string:screenid>')
def show_screen_legacy(screenid):
    return show_screen(screenid)

@app.route('/view/<string:screenid>')
def show_screen(screenid):
  with open('screens/' + screenid + '.html', 'r') as myfile:
    data = myfile.read()
  subtemplate = env.from_string(data)
  subdata = subtemplate.render(**request.args)
  #subdata = render_template_string(data, undefined=SilentUndefined, **request.args)

  #return render_template('main.html', body=subdata, undefined=SilentUndefined, **request.args)
  return render_template('main.html', body=subdata, screenid=screenid, undefined=SilentUndefined, **request.args)

def setup_drivers():
  available_modules = [d for d in inspect.getmembers(drivers) if inspect.ismodule(d[1])]
  available_drivers = {}
  for module in available_modules:
    for member in inspect.getmembers(module[1]):
      if inspect.isclass(member[1]):
        if member[0] == module[0]:
          available_drivers[module[0]] = member[1]
          break
  driver_data = json.load(open('config/drivers.json'))  
  for driver_name, driver_cfg in driver_data.items():
    if driver_cfg['driver'] in available_drivers:
      sources[driver_name] = available_drivers[driver_cfg['driver']](driver_cfg['cfg'])
    else:
      raise Exception('Invalid Driver Class: ' + str(driver_cfg['driver']))


def run_periodics(source_list):
  time.sleep(1)
  while True:
    for source in source_list:
      source_list[source].tick(source_list)
    time.sleep(TICKRATE)

if __name__ == '__main__':
  setup_drivers()
  #thread.start_new_thread(run_periodics, (sources,))
  threading.Thread(target=run_periodics, args=(sources,)).start()
  #app.run(debug=True, use_reloader=False, host='0.0.0.0', port=8000)
  waitress.serve(app, listen='0.0.0.0:8000') 

