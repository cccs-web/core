                <script>
                    $(function() {
                        var data = {{ country_projects | safe }},countryChart, mapChart;
                        var mapData = Highcharts.geojson(Highcharts.maps['custom/world-highres']);
                        var overall_data = [];
                        var country_data = {{ country_categorization | safe }};
                            {% for super_name, super_info in categorization.items %}
                                overall_data.push(['{{super_name|safe}}', {{super_info.count|safe}}]);
                            {% endfor %}
                            $.each(mapData, function () {
                                this.id = this.properties['hc-key']; // for Chart.get()
                                this.flag = this.id.replace('UK', 'GB').toLowerCase();
                            });

                            // Wrap point.select to get to the total selected points
                            Highcharts.wrap(Highcharts.Point.prototype, 'select', function (proceed) {

                                proceed.apply(this, Array.prototype.slice.call(arguments, 1));

                                var points = mapChart.getSelectedPoints();

                                if (points.length) {
                                    if (points.length === 1) {
                                        $('#info #flag').attr('class', 'flag ' + points[0].flag);
                                        $('#info h2').html(points[0].name);
                                        countryChart.series[0].update({data: country_data[points[0].code3]});
                                        countryChart.redraw();
                                    }

                                } else {
                                    $('#info #flag').attr('class', '');
                                    $('#info h2').html('Overall');
                                    countryChart.series[0].update({data: overall_data});
                                    countryChart.redraw();
                                }
                            });
                            // Initiate the map chart
                            mapChart = $('#map_container').highcharts('Map', {

                                title : {
                                    text : 'Projects by {{ categorization_name }}'
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

                                series : [{
                                    data : data,
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

                            countryChart = $('#country-chart').highcharts({
                                chart: {
                                    plotBackgroundColor: null,
                                    plotBorderWidth: null,
                                    plotShadow: false
                                },
                                title: {
                                    text: null
                                },
                                tooltip: {
                                    pointFormat: 'count: <b>{point.y}</b>, share: <b>{point.percentage:.1f}%</b>'
                                },
                                legend: {

                                    width: '100%',
                                    itemWidth: '100%'
                                },
                                plotOptions: {
                                    pie: {
                                        allowPointSelect: true,
                                        cursor: 'pointer',
                                        dataLabels: {
                                            enabled: false,
                                            format: '<b>{point.name}</b>: {point.y}',
                                            style: {
                                                color: (Highcharts.theme && Highcharts.them.contrastTextColor) || 'black'
                                            }
                                        }
                                    }
                                },
                                series: [{
                                    type: 'pie',
                                    name: '',
                                    data: overall_data,
                                    showInLegend: true
                                }]
                            }).highcharts();

                    });
                </script>
