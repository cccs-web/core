<script>
    $(function() {
        var data = {{country_projects | safe}},countryChart, mapChart;
        var mapData = Highcharts.geojson(Highcharts.maps['custom/world-highres']);
        var overall_data = [];
        var overall_data_drill = [];
        var country_data = {{country_categorization | safe}};
        var country_data_all = {};
        for (var code in country_data) {
            var series = [], drilldown_rows = [];
            var _data = country_data[code];
            for (key in _data) {
                series.push({
                    name: key,
                    y: _data[key].count,
                    drilldown: key
                });
                var drilldown = _data[key]['drilldown'];
                var drilldown_row = {
                    id: key,
                    name: key
                };
                var d = [];
                for (sub_key in drilldown) {
                    d.push({
                        name: sub_key,
                        y: drilldown[sub_key],
                        visible: true
                    });
                }
                drilldown_row['data'] = d;
                drilldown_rows.push(drilldown_row);
            }
            country_data_all[code] = {series: series, drilldown: drilldown_rows};
        }

        $.each(mapData, function() {
            this.id = this.properties['hc-key']; // for Chart.get()
            this.flag = this.id.replace('UK', 'GB').toLowerCase();
        });

        // Wrap point.select to get to the total selected points
        Highcharts.wrap(Highcharts.Point.prototype, 'select', function(proceed) {

            proceed.apply(this, Array.prototype.slice.call(arguments, 1));

            var points = mapChart.getSelectedPoints();

            if (points.length) {
                if (points.length === 1) {
                    $('#info #flag').attr('class', 'flag ' + points[0].flag);
                    $('#info h2').html(points[0].name);
                    countryChart.destroy();
                    var cd = country_data_all[points[0].code3];
                    console.log(cd);
                    countryChart = $('#country-chart').highcharts({
                        chart: {
                            type: 'pie'
                        },
                        title: {
                            text: 'Projects by {{ categorization_name }}'
                        },
                        plotOptions: {
                            series: {
                                dataLabels: {
                                    enabled: true,
                                    format: '{point.name}: {point.y}'
                                }
                            }
                        },

                        tooltip: {
                            headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                            pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of {point.total}<br/>'
                        },
                        series: [{
                            name: '{{ categorization_name }}',
                            data: cd.series,
                            colorByPoint: true
                        }],
                        drilldown: {
                            series: cd.drilldown
                        }
                    }).highcharts();

                }

            } else {
                $('#info #flag').attr('class', '');
                $('#info h2').html('Overall');
                countryChart.destroy();
                countryChart = $('#country-chart').highcharts({
                    chart: {
                        type: 'pie'
                    },
                    title: {
                        text: 'Projects by {{ categorization_name }}'
                    },
                    plotOptions: {
                        series: {
                            dataLabels: {
                                enabled: true,
                                format: '{point.name}: {point.y}'
                            }
                        }
                    },

                    tooltip: {
                        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                        pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of {point.total}<br/>'
                    },
                    series: [{
                        name: '{{ categorization_name }}',
                        data: overall_data,
                        colorByPoint: true
                    }],
                    drilldown: {
                        series: overall_data_drill
                    }
                }).highcharts();
            }
        });

        // Initiate the map chart
        mapChart = $('#map_container').highcharts('Map', {
            title: {
                text: 'Projects by {{ categorization_name }}'
            },
            mapNavigation: {
                enabled: true,
                buttonOptions: {
                    verticalAlign: 'bottom'
                }
            },

            colorAxis: {
                endOnTick: false,
                startOnTick: false
            },

            tooltip: {
                footerFormat: '<span style="font-size: 10px">(Click for details)</span>'
            },

            series: [{
                data: data,
                mapData: mapData,
                joinBy: ['iso-a3', 'code3'],
                name: 'Projects',
                allowPointSelect: true,
                cursor: 'pointer',
                states: {
                    select: {
                        color: '#a4edba',
                        borderColor: 'black',
                        dashStyle: 'shortdot'
                    }
                }
            }]
        }).highcharts();


        {% for super_name, super_info in categorization.items %}
            overall_data.push({
                name: '{{ super_name | safe }}',
                y: {{ super_info.count | safe }},
                drilldown: '{{ super_name | safe }}'
            });
            j = 0;
            var drilldown = {
                id: '{{ super_name | safe }}',
                name: '{{super_name | safe}}'
            };
            var data = [];
            {% for sub_name, sub_info in super_info.subs.items %}
                data.push({
                    name: '{{ sub_name | safe }}',
                    y: {{ sub_info.count }},
                    visible: true
                });
            {% endfor %}

            drilldown['data'] = data;
            overall_data_drill.push(drilldown);
        {% endfor %}

        countryChart = $('#country-chart').highcharts({
            chart: {
                type: 'pie'
            },
            title: {
                text: 'Projects by {{ categorization_name }}'
            },
            plotOptions: {
                series: {
                    dataLabels: {
                        enabled: true,
                        format: '{point.name}: {point.y}'
                    }
                }
            },

            tooltip: {
                headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> of {point.total}<br/>'
            },
            series: [{
                name: '{{ categorization_name }}',
                data: overall_data,
                colorByPoint: true
            }],
            drilldown: {
                series: overall_data_drill
            }
        }).highcharts();
    });
</script>