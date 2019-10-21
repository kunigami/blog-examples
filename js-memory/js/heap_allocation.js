window.onload = function() {

    var container = document.createElement("container");
    document.body.appendChild(container);

    var append = function(container, append) {
        var p = document.createElement('p');
        p.data = new Array(10000);
        for (var j = 0, l = p.data.length; j < l; ++j) {
            p.data[j] = j.toString();
        }
        container.appendChild(p);
    };
    var remove = function(container) {
        var first = container.firstChild;
        container.removeChild(first);
    }

    var content = document.createElement('div');

    var showDiv = document.createElement('div');

    var buttonAppend = document.createElement('button');
    buttonAppend.type = "button";
    buttonAppend.onclick = append.bind(null, content);
    buttonAppend.innerHTML = 'Append';

    var buttonRemove = document.createElement('button');
    buttonRemove.type = "button";
    buttonRemove.onclick = remove.bind(null, content);
    buttonRemove.innerHTML = 'Remove';

    container.appendChild(buttonAppend);
    container.appendChild(buttonRemove);
}
