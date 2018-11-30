// JavaScript Document

$(function () {
    var myChart = echarts.init(document.getElementById('main'),'dark');
    myChart.showLoading();
    $.get('../static/data/page_rank.gexf', function (xml) {//les-miserables  six
        myChart.hideLoading();
        var graph = echarts.dataTool.gexf.parse(xml);
        var categories = [];
        for (var i = 0; i < 5; i++) {
            categories[i] = {
                name: '可信度' + i
            };
        }
        console.log(graph.links);
        graph.nodes.forEach(function (node) {
            node.itemStyle = null;
            // node.value = 10;
            //  node.value = node.attributes.trust_value;
            node.value = node.symbolSize;
            node.symbolSize /= 1.5;
            node.label = {
                normal: {
                    show: node.symbolSize > 30
                }
            };
            node.draggable = true;
            node.category = node.attributes.modularity_class;
            // node.category = 0;//跟 legend 联系在一起 legend 有几个，这边就有几个 数组；
        });
        mytextStyle = {
            color: '#fff',                           //文字颜色
            fontStyle: "normal",                     //italic斜体  oblique倾斜
            fontWeight: "bolder",                    //文字粗细bold   bolder   lighter  100 | 200 | 300 | 400...
            fontFamily: "Helvetica",                //字体系列
            fontSize: 18,                              //字体大小
        };

        option = {
            title: {
                text: '用户信任度聚类分析',
                subtext: '数据来源于Adgovato',
                sublink: "http://127.0.0.1:9999/evaluation_2",
                textStyle:mytextStyle,
                z: 2,
                top: '14%',
                left: '68%',
                color: 'white',
                borderColor: "#000",
                borderWidth: 0,
                shadowColor: "red",
            },
            tooltip: {},
            legend: [{
                // selectedMode: 'single',
                orient: 'vertical',
                x: '10%',
                y: '30%',
                textStyle: {
                    color: '#fff'          // 图例文字颜色
                },
                size: 10,
                data: categories.map(function (a) {//  map() 方法返回一个由原数组中的每个元素调用一个指定方法后的返回值组成的新数组。
                    return a.name;
                })
            }],
            animationDuration: 5000,
            animationEasingUpdate: 'quinticInOut',
            series: [
                {
                    name: '实验数据',
                    type: 'graph',
                    layout: 'circular',
                    circular: {
                        rotateLabel: true
                    },
                    // force\circular
                    data: graph.nodes,
                    links: graph.links,
                    categories: categories,
                    roam: true,
                    focusNodeAdjacency: true,
                    itemStyle: {
                        normal: {
                            borderColor: '#FFC',
                            borderWidth: 1,
                            shadowBlur: 10,
                            shadowColor: 'rgba(0, 0, 0, 0.3)',
                            opacity: 1.0
                        }
                    },
                    label: {
                        normal: {
                            position: 'right',
                            formatter: '{b}'
                        }
                    },
                    lineStyle: {
                        normal: {
                            show: 'true',
                            color: 'source',
                            curveness: 0.2,
                            width: 1.5,
                        }
                    },
                    force: {
                        edgeLength: [100, 150],
                        repulsion: 200
                    },
                    emphasis: {
                        lineStyle: {
                            width: 10,
                        }
                    }
                }
            ]
        };
        myChart.setOption(option);
    }, 'text');
})