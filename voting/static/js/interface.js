function giveFeedback(msg){
    if($("#feedback").length ===0){
        $("body").append(makeAlertModal("feedback", msg).join(""));
    }else{
        $("#feedback").find('.alert').html(msg);
    }
    $('#feedback').modal('show');
}

function makeAlertModal(id, msg){
    var header = new Array(), body = new Array(), footer = new Array();
    header.push('<h3 id="myModalLabel">Feedback</h3>');
    body.push('<div class="alert">');
    body.push(msg);
    body.push('</div>');
    return makeModalWindow(id, header, body, footer);
}

function makeModalWindow(id, header, body, footer){
    var form = new Array();
    form.push('<div class="modal hide fade" id="'+id+'" tabindex="-1" role="dialog" aria-labelledby="formModalLabel" aria-hidden="true">');
    form.push('<div class="modal-header">');
    form.push('<button type="button" class="close" data-dismiss="modal" aria-hidden="true">x</button>');
    form.push('<h3 id="myModalLabel">');
    form = form.concat(header);
    form.push('</h3>');
    form.push('</div>');
    form.push('<div class="modal-body">');
    form.push('<p>');
    form = form.concat(body);
    form.push('</p></div>');
    form.push('<div class="modal-footer">');
    form = form.concat(footer);
    form.push('</div></div>');
    return form;
}

function makeWindow(url, title, wdth, hght, element, dataString){

    var htmlData = getAjaxData(url, dataString, null);
    makeHtmlWindow(htmlData, title, wdth, hght, element)
}

function makeHtmlWindow(data, title, wdth, hght, element){

    $('<div id="'+element+'" title="'+title+'" class="ui-dialog-title"></div>').appendTo($('body'));
    var div = "#"+element;
    $(div).html(data);
    openWindow(element, title, wdth, hght);  
}

function getAjaxData(url, dataString, type){
    var htmlData = null;
    if(type == null){
        type = 'html';
    }
    $.ajax({
        type: 'POST',
        data: dataString,
        url: url,
        dataType: type,
        async: false,
        success: function(data) {
            htmlData = data;
        }
    });
    return htmlData;
}

function openWindow(element, title,  wdth, hght){
    var div = "#"+element;
    $(div).dialog({
        autoOpen: false,
        height: hght,
        width: wdth,
        zIndex: 9999, 
        modal: false,
        "title": title
    }); 
  
    $( div ).dialog( "open" );  
}

function findHtmlByDiv(url, divTitle, divContent){
    var els = new Array();
    var data = getAjaxData(url, null, "html");
    var par = $(data).find(divTitle);
    //els[0] = par.text();
    els[0] = par;
    els[1] = $(data).find(divContent);
    return els;
}

/**
 * function for fixing the ajax requests for django
 **/
function fixAjax(event, xhr, settings) {
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  function sameOrigin(url) {
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
  }
  function safeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
  }
}


var Grapher = function(id, data){
    this.id = id;
    this.data = data;
}


Grapher.prototype.createPieChart = function(xaxis, yaxis){
    var data = this.data;
    var w = 400, h = 400, r = 200, color = d3.scale.category20c();
  
    var vis = d3.select("#"+this.id)
        .append("svg:svg")              //create the SVG element inside the <body>
        .data([data])                   //associate our data with the document
            .attr("width", w)           //set the width and height of our visualization (these will be attributes of the <svg> tag
            .attr("height", h)
        .append("svg:g")                //make a group to hold our pie chart
            .attr("transform", "translate(" + r + "," + r + ")")    //move the center of the pie chart from 0, 0 to radius, radius
 
    var arc = d3.svg.arc()              //this will create <path> elements for us using arc data
      .outerRadius(r);
 
    var pie = d3.layout.pie()           //this will create arc data for us given a list of values
      .value(function(d) { return d[yaxis]; });    //we must tell it out to access the value of each element in our data array
 
    var arcs = vis.selectAll("g.slice")     //this selects all <g> elements with class slice (there aren't any yet)
      .data(pie)                          //associate the generated pie data (an array of arcs, each having startAngle, endAngle and value properties) 
      .enter()                            //this will create <g> elements for every "extra" data element that should be associated with a selection. The result is creating a <g> for every object in the data array
          .append("svg:g")                //create a group to hold each slice (we will have a <path> and a <text> element associated with each slice)
              .attr("class", "slice");    //allow us to style things in the slices (like text)
 
    arcs.append("svg:path")
          .attr("fill", function(d, i) { return color(i); } ) //set the color for each slice to be chosen from the color function defined above
          .attr("d", arc);                                    //this creates the actual SVG path using the associated data (pie) with the arc drawing function
 
    arcs.append("svg:text")                                     //add a label to each slice
        .attr("transform", function(d) {                    //set the label's origin to the center of the arc
          //we have to make sure to set these before calling arc.centroid
          d.innerRadius = 0;
          d.outerRadius = r;
          return "translate(" + arc.centroid(d) + ")";        //this gives us a pair of coordinates like [50, 50]
      })
      .attr("text-anchor", "middle")                          //center the text on it's origin
      .text(function(d, i) { return data[i][xaxis]; });
}

Grapher.prototype.createBarChart = function(xaxis, yaxis){
    
    var data = this.prepareDataForBar();
    
    var margin = 50, width = 400, height = 400;
    
    if(yaxis == "frequency"){
      var formatPercent = d3.format(".0%");
    }else{
      var formatPercent = d3.format(".2s")
    }
  
    var x = d3.scale.ordinal().rangeRoundBands([0, width], .1);
    var y = d3.scale.linear().range([height, 0]);
  
    var xAxis = d3.svg.axis().scale(x).orient("bottom");
    var yAxis = d3.svg.axis().scale(y).orient("left").tickFormat(formatPercent);
  
    var svg = d3.select("#"+this.id).append("svg")
        .attr("width", width + margin + margin)
        .attr("height", height + margin + margin)
      .append("g")
        .attr("transform", "translate(" + margin + "," + margin + ")");
    
    data.forEach(function(d) {
      d.sepalWidth = +d[yaxis];
    });
    
    x.domain(data.map(function(d) { return d[xaxis]; }));
    y.domain([0, d3.max(data, function(d) { return d[yaxis]; })]);
    
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);
  
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text(yaxis);
  
    svg.selectAll(".bar")
        .data(data)
      .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d[xaxis]); })
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d[yaxis]); })
        .attr("height", function(d) { return height - y(d[yaxis]); });
}

Grapher.prototype.prepareDataForBar = function(){
    var new_data = new Array();
    for(var i=0; i<this.data.length; i++){
        var obj = {"candidate": this.data[i][1], "votes": this.data[i][0]}
        new_data.push(obj);
    }
    return new_data;
}
