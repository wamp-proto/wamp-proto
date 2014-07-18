import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import json


TEMPLATE = """
<!doctype html>
<html>
   <head>
      <style>
         {0}
      </style>
   </head>
   <body>
      {1}
   </body>
</html>
"""

class MyRenderer(mistune.Renderer):

   def format_wamp_code(self, obj):
         r = []
         if obj['type'] == 'procedure':
            r.append("<h2>Procedure {}</h2>".format(obj['uri']))
         elif obj['type'] == 'topic':
            r.append("<h2>Topic {}</h2>".format(obj['uri']))
         else:
            pass

         args = obj.get('args', [])
         if len(args) > 0:
            r.append('<ul class="wamp_args">')
            for arg in args:
               r.append('<li>{}</li>'.format(arg['help']))
            r.append('</ul>')

         kwargs = obj.get('kwargs', [])
         if len(kwargs) > 0:
            r.append('<ul class="wamp_kwargs">')
            for arg in kwargs:
               r.append('<li>{}</li>'.format(arg['help']))
            r.append('</ul>')

         return '\n'.join(r)


   def block_code(self, code, lang):
      if not lang:
         return "\n<pre><code>{}</code></pre>\n".format(mistune.escape(code))

      if lang == 'javascript':
         try:
            obj = json.loads(code)
         except Exception as e:
            pass
         else:
            if type(obj) == dict and 'uri' in obj:
               return self.format_wamp_code(obj)

      lexer = get_lexer_by_name(lang, stripall=True)
      formatter = HtmlFormatter()
      return highlight(code, lexer, formatter)



if __name__ == '__main__':
   renderer = MyRenderer()
   md = mistune.Markdown(renderer = renderer)
   with open('test2.md', 'r') as f:
      source = f.read()
      content = md.render(source)
      css = HtmlFormatter().get_style_defs('.highlight')
      generated = TEMPLATE.format(css, content)
      with open('test2.html', 'w') as t:
         t.write(generated)
