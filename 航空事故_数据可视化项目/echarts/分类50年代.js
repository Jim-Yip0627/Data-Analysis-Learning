var dom = document.getElementById("分类50年代");
var myChart50s = echarts.init(dom);
var app = {};
option = null;
var data = [
    {
        name: '飞机完全损毁',
        children: [
        {
            name:'军用',
            children:[
            {
                    name: '操作失误',
                    value: 3,
                }, {
                    name: '外部干扰',
                    value: 1,
                },
            ]
        },
        {
            name:'民用航空',
            children:[
            {
                    name: '操作失误',
                    value: 23,
                }, {
                    name: '外部干扰',
                    value: 1,
                }, 
            ]
        },
        {
            name: '通用航空',
            children:[
            {
                    name: '操作失误',
                    value: 32,
                }, {
                    name: '外部干扰',
                    value: 3,
                }, 
            ]
        },
    ]}, 

    {
        name:'未损毁',
        children:[
            {
                name:'民用航空',
                children:[
                {name: '操作失误',
                    value: 2,
                }, {
                    name: '外部干扰',
                    value: 2,
                }
                ]
            },
            {
                name:'通用航空',
                children:[
                    {
                        name:'操作失误',
                        value:2,
                    }
                ]
            },
        ]
    }
];

option = {
    title: {
        text: '20-50年代事故类型、原因分类',
        //subtext: '数据来源于asn与世界银行数据库',
        x:'center',
        y: 'bottom',
    },

    visualMap: {
        type: 'continuous',
        min: 1,
        max: 80,
        inRange: {
            color: ['#4592af','#33313b',]
        }
    },
    series: {
        type: 'sunburst',
        highlightPolicy: 'ancestor',
        data: data,
        radius: [0, '95%'],
        sort: null,
        levels: [{}, {
            r0: '15%',
            r: '35%',
            itemStyle: {
                borderWidth: 2
            },
            label: {
                rotate: 'tangential'
            }
        }, {
            r0: '35%',
            r: '70%',
            label: {
                align: 'right'
            }
        }, {
            r0: '70%',
            r: '72%',
            label: {
                position: 'outside',
                padding: 3,
                silent: false
            },
            itemStyle: {
                borderWidth: 3
            }
        }]
    }}
;
myChart50s.setOption(option);

