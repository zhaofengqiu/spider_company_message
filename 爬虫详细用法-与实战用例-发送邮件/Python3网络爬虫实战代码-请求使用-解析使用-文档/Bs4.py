from bs4 import BeautifulSoup

html = """
<div class="panel">
    <div class="panel-heading">
        <h4>Hello</h4>
    <div>
    <div class="panel-body">
        <ul class="list" id="list-1">
            <li class="element">AA</li>
            <li class="element">BB</li>
            <li class="element">CC</li>
        </ul>
        <ul class="list" id="list-2">
            <li class="element">EE</li>
            <li class="element">FF</li>
        </ul>
    </div>
</div>
"""


so = BeautifulSoup(html,'lxml')
for ul in so.select('ul'):
    print(ul['id'])
    print(ul.attrs['id'])