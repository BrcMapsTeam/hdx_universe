function forceGraph(nodes,links){

  var initialDrag = true;

  width = $('body').width();
  height = $('#map').height();

  var force = d3.layout.force()
      .charge(-2000)
      .linkDistance(400)
      .size([width, height]);

  var scale = 1/Math.pow(nodes.length,0.3);
  var scale = 0.02

  var zoomWidth = width/2*(1-scale)
  var zoomHeight = height/2*(1-scale)

  zoom.translate([zoomWidth,zoomHeight]).scale(scale);

  var svg = d3.select('#map').append("svg")
      .attr("width", width)
      .attr("height", height)
      .call(zoom.on("zoom", redraw))
        .append('g')
        .attr("transform","translate("+zoomWidth+","+zoomHeight+") scale("+scale+","+scale+")");

  force
      .nodes(nodes)
      .links(links)
      .start();

  force.on("tick", function() {
      tick++
      $('#loadingpercent').html(Math.round(tick/3));
  });

  $('#zoom-in').on('click',function(){
    mapZoom('in');
  });
  $('#zoom-out').on('click',function(){
    mapZoom('out');
  });

  $('#play').on('click',function(){
    console.log('play');
    if(!play){
      $('#play').html('⏹');
      play = true;
      playmode();
    } else {
      $('#play').html('▶');
      play = false;
    }
  });

  function mapZoom(zoomType){
    if(zoomType=='in'){
      zoom.scale(zoom.scale()*1.5);
    } else {
      zoom.scale(zoom.scale()/1.5);
    }
    redraw();
  }

  force
      .on('end', function() {

        $('#intro-text').remove();
        $('#loader').remove();
        $('.sp').remove();

        var link = svg.selectAll(".link")
          .data(links)
          .enter().append("line")
          .attr("class", "link")
          .style("stroke-width", function(d) {
            if(d.value>10){
              return 10
            } else {
              return d.value;
            }
          });

        var node = svg.selectAll(".node")
            .data(nodes)
            .enter().append("circle")
            .attr("id",function(d,i){
              return "node"+i;
            })
            .attr("class", function(d){
              return "node ";
            })
            .attr("r", function(d,i) {
                return 20+Math.sqrt(d.d)*2;
            })
            .style("stroke",function(d){
              if(d.h==1){
                return '#E53935';
              } else {
                return 'black';
              }
            })
            .style("fill",function(d){
              if(d.h==1){
                return '#E53935';
              } else {
                return 'black';
              }
            })            
            .style("stroke-width",2);

        link.attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });

        node.attr("cx", function(d) { return d.x; })
          .attr("cy", function(d) { return d.y; });

        node.on("mouseover",function(d){
          if(!play){
            showinfo(d);
          }
        });

        node.on("mouseout",function(d){
          if(!play){
            $('#info_overlay').html('<p>Hover a point for more info</p>');
          }
        });

        node.on("click",function(d){
          window.open("https://data.humdata.org/dataset/"+d.i);
        });



        kmeans(30,svg);


      });

    force
      .on('start', function(){
        d3.selectAll('.cluster').remove();
      })

  return svg;
}

let nodeCall = $.ajax({ 
    type: 'GET', 
    url: 'data/hdxDataScrape.json',
    dataType: 'json',
});

let linkCall = $.ajax({ 
    type: 'GET', 
    url: 'data/hdxDataLinks2.json',
    dataType: 'json',
});

var zoom = d3.behavior.zoom();

var nodes = [];
var links = [];
var tick = 0;

var width;
var height;
var svg;
var play = false;

console.log($(window).height());
$('#map').height(Math.max($(window).height(),600));

$.when(nodeCall,linkCall).then(function(nodeArgs,linkArgs){
  links = linkArgs[0];
  nodes = nodeArgs[0];
  links.forEach(function(d){
    d.source = d.s;
    d.target = d.t;
    d.value = d.v;
  });
  $('#loader').html('Simulating Graph <span id="loadingpercent">0</span>%');
  svg = forceGraph(nodes,links);
});

function kmeans(clusternum,svg){
  var maxX = d3.max(nodes,function(d){return d.x});
  var maxY = d3.max(nodes,function(d){return d.y});
  var minX = d3.min(nodes,function(d){return d.x});
  var minY = d3.min(nodes,function(d){return d.y});
  var clusters = [];
  for(i=0;i<clusternum;i++){
    clusters.push({'x':Math.random()*(maxX-minX)+minX,'y':Math.random()*(maxY-minY)+minY,'count':0,'rx':0,'ry':0,'tags':{},'bbox':[0,0,0,0]});
  }

  var change = true;
  var n=0;
  while(change==true&&n<10){
    n++
    change=false;
    clusters.forEach(function(c){
      c['count'] = 0;
      c['rx'] = 0;
      c['ry'] = 0;
    });
    nodes.forEach(function(d){
        clusters.forEach(function(c,i){
          distance = Math.sqrt(Math.pow((d.x-c.x),2)+Math.pow((d.y-c.y),2));

          if(i==0){
            closest = 0;
            closestDistance = distance;
          } else {
            if(distance<closestDistance){
              closest=i;
              closestDistance = distance;
            }
          }
        });
        if(closest!=d.cluster){
          change=true;
        }
        d.cluster=closest;
        clusters[closest].count++;
        clusters[closest].rx+=d.x;
        clusters[closest].ry+=d.y;
    });

    clusters.forEach(function(c){
      c.x=c.rx/c.count;
      c.y=c.ry/c.count;
    });

  }
  
  nodes.forEach(function(d){
      d.t.forEach(function(t){
        if(!(t in clusters[d.cluster].tags)){
          clusters[d.cluster].tags[t] = 1;
        } else {
          clusters[d.cluster].tags[t]++
        }
      });
  });

  clusters.forEach(function(d){
    var tag = '';
    var max=0;
    var oldtag = '';
    var oldmax=0;
    for(key in d.tags){
      if(max<d.tags[key]){
        oldtag = tag;
        oldmax = max;
        max = d.tags[key];
        tag = key;

      }
    }
    if(oldmax/max>0.7){
      d.label = tag + ' & ' + oldtag;
    } else {
      d.label = tag;
    }
  });

  var clustertext = svg.append("g").selectAll("cluster")
      .data(clusters)
      .enter()

  scale = zoom.scale();
  if(scale<0.03){
    scale = 0.03;
  }

  var recs = clustertext.append("rect")
    .attr("x", function(d) { return d.x; })
        .attr("y", function(d) { return d.y-15/scale; })
      .attr("width", function(d){return 0})
      .attr("height", function(d){return 0})
      .attr("class","cluster clusterrec")
      .style("fill", "black")
      .on('click',function(d,i){
          zoomToCluster(i,d.label);
        });

  clustertext.append("text")
      .attr("x", function(d) { return d.x; })
        .attr("y", function(d) { return d.y; })
        .text( function (d) { return d.label; })
        .attr("font-size", function(d){
          var size = 15/scale;
          return size + 'px';
        })
        .attr("fill", "white")
        .attr("class","cluster")
        .on('click',function(d,i){
          zoomToCluster(i,d.label);
        })
        .call(getBB);

    recs.attr("width", function(d){return d.bbox.width/scale})
      .attr("height", function(d){return d.bbox.height/scale})

  var fail = 0;

  clusters.forEach(function(c){
    if(isNaN(c.x)){
      fail++;
    }
  });
  if(fail>10){
    kmeans(30,svg);
  }

  function getBB(selection) {

      scale = zoom.scale();
      if(scale<0.03){
        scale = 0.03;
      }
      selection.each(function(d){
        d.bbox = this.getBBox();
        d.bbox.width=d.bbox.width*scale;
        d.bbox.height=d.bbox.height*scale;
      })
  }
}

function playmode(){
  show();
}

function show(){
  if(play){
    node = Math.floor(Math.random() * nodes.length);
    zoomToNode(node);
    setTimeout(function(){
      show()}, 12000);
  }
}

function zoomToNode(id){
  d3.selectAll('.node').style('stroke-width','0');
  d3.select();
  $('#info_overlay').html('<p>Press pause to explore the map</p>');
  var scale = 0.02
  var zoomWidth=(0*-1*scale+width/2);
  var zoomHeight = (0*-1*scale+height/2);
  zoom.translate([zoomWidth,zoomHeight]);
  zoom.scale(scale);
  d3.select('#node'+id).style('stroke','#03A9F4').style('stroke-width','8');

  svg.transition().duration(1500).attr("transform",
          "translate("+zoomWidth+","+zoomHeight+") scale("+scale+","+scale+")").call(endall,
          function() {
            redraw();
            var scale = 0.5
            var zoomWidth=(nodes[id].x*-1*scale+width/2);
            var zoomHeight = (nodes[id].y*-1*scale+height/2);
            zoom.translate([zoomWidth,zoomHeight]);
            zoom.scale(scale);
            svg.transition().duration(4000).attr("transform",
                    "translate("+zoomWidth+","+zoomHeight+") scale("+scale+","+scale+")").call(endall,
                    function() {
                      redraw();
                      showinfo(nodes[id]);
                    });
          });
  

  //redraw();
  /*var size = 15/scale;

    d3.selectAll('.cluster').attr("font-size", function(d){
        return size + 'px';
    });

    d3.selectAll('.clusterrec').attr("width", function(d){return d.bbox.width/scale })
        .attr("height", function(d){return d.bbox.height/scale})
        .attr("y", function(d) { return d.y-15/scale; });*/

}

function showinfo(d){
  $('#info_overlay').html('<p>'+d.n+'</p><p>'+d.o+'</p><p>Downloads: '+d.d+'</p><p id="notes"></p><p>Click to see on HDX</p>');
  $.ajax({
    url: "data/description/"+d.i+".json",
    success: function(result){
      $("#notes").html(result['notes']);
    }
  });
}

function redraw() {
    var translate = zoom.translate();
    var scale = zoom.scale();
    if(d3.event){
      translate = d3.event.translate;
      scale = d3.event.scale;
    }


    svg.attr("transform",
      "translate(" + translate + ")"
      + " scale(" + scale + ")");

    var scale = zoom.scale()
    if(scale<0.03){
      scale = 0.03;
    }

    var size = 15/scale;

    d3.selectAll('.cluster').attr("font-size", function(d){
      return size + 'px';
    })

    d3.selectAll('.clusterrec').attr("width", function(d){return d.bbox.width/scale })
      .attr("height", function(d){return d.bbox.height/scale})
      .attr("y", function(d) { return d.y-15/scale; })
}

function endall(transition, callback) {
      if (!callback) callback = function(){};
      if (transition.size() === 0) { callback() }
    var n = 0;
    transition
        .each(function() { ++n; })
        .each("end", function() { if (!--n) callback.apply(this, arguments);});
}
