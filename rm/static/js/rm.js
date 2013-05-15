// Main Randomise.me Javascript file.
//

var RM = {

    forms :{
        init_modalreports: function(){
            $('form.ajaxform').ajaxForm({

                beforeSubmit: function(arr, $form, options){

                    var valid = _.every(
                        $('.modal.in .modal-body input:visible'),
                        function(el){
                            return $(el).parsley('destroy').parsley('validate') !== false
                        });

                    if(!valid){
                        return false;
                    }else{
                        return true;
                    }
                },

                success: function(data){
                    var active = $('.modal.in');
                    var period = $('a[href$="'+active.attr('id')+'"]');
                    var status = period.children('p').children('i')
                    period.attr('href', '#').attr('data-toggle', '').attr('role', '')
                    status.toggleClass('icon-ok-sign')
                    active.modal('toggle');
                    console.log('ta!');
                    console.log(active);
                },

                error: function(data){
                    console.log('nah!')
                    console.log(data);
                },

            })
        },

        init_instruction_toggles : function(){
            $('input[name="instruction_delivery"]').change(
                function(e){
                    var hidem = function(){
                        $('#hours-after-container').hide();
                        $('#instruction-date-container').hide();
                    }
                    var showem = function(sel){$(sel).show()}

                    console.log(e)
                    var src = $(e.target);
                    if(src.attr('value') == 'im'){
                        hidem()
                    }else if(src.attr('value') == 'ho'){
                        hidem();
                        showem('#hours-after-container');
                    }else{
                        hidem();
                        showem('#instruction-date-container');
                    }
                }
            )
        },

    },

    graphs: {
        single_user_trial: function(selector, data){
            RM.graphs.trial_bar(selector, data, 420, 60)
            },

        trial_thumbnail: function(selector, data){
            RM.graphs.trial_bar(selector, data, 210, 30)
        },

        trial_report: function(pk, results){
            var bar_selector = "#mainbar-"+ pk;
            RM.graphs.trial_vertical_bar(bar_selector, results, 600, 300)
        },

        trial_vertical_bar: function(selector, data, width, height){

            var x = d3.scale.ordinal()
                .domain(_.pluck(data, 'name'))
                .rangeRoundBands([0, width], .1);

            var ydomain = [0, _.max(_.pluck(data, 'avg'))]

            var y = d3.scale.linear()
                .domain(ydomain)
                .range([height, 0]);

            var xAxis = d3.svg.axis()
                .scale(x)
                .orient('bottom');

            var yAxis = d3.svg.axis()
                .scale(y)
                .orient('left');

            var chart = d3.select(selector).append('svg')
                .attr('class', 'chart')
                .attr('width',  width +30+30+30)
                .attr('height', height + 30+30+30)
                .append('g')
                .attr('transform', 'translate(60,60)');

            chart.append('g')
                .attr('class', 'x axis')
                .attr('transform', 'translate(0,'+height +')')
                .call(xAxis);

            chart.append('g')
                .attr('class', 'y axis')
                .call(yAxis)
                // .append('text')
                // .attr('transform', 'rotate(-90)')
                // .attr('y', 6)
                // .attr('dy', '.71em')
                // .style('text-anchor', 'end')
                // .text('Score');

            chart.selectAll('.bar')
                .data(data)
              .enter().append('rect')
                .attr('class', 'bar')
                .attr('x', function(d){ return x(d.name); })
                .attr('width', x.rangeBand())
                .attr('y', function(d) { return y(d.avg); })
                .attr('height', function(d) { return height - y(d.avg); } )
        },

        trial_bar: function(selector, data, width, height){

            var chart = d3.select(selector).append('svg')
                        .attr('class', 'chart')
                        .attr('width', width)
                        .attr('height', height * data.length);

            var x = d3.scale.linear()
                    .domain([0, d3.max(_.pluck(data, 'avg'))])
                    .range([0, width]);

            // var y = d3.scale.ordinal()
            //     .domain(_.pluck(data, 'name'))
            //     .rangeBands([0, 120]);

            chart.selectAll('rect')
                .data(data)
                .enter().append('rect')
            .attr('y', function(d, i){ return i * height; })
            .attr('width', function(d) { return x(d.avg)})
            .attr('height', height)

            chart.selectAll('text')
                .data(data)
                .enter().append('text')
                .attr('x', function(d) { return x(d.avg); })
                .attr('y', function(d, i) { return i * height + height / 2 })
                .attr('dx', -3)
                .attr('dy', '.35em')
                .attr('text-anchor', 'end')
                .text(function(d) { return d.name + ' (' + d.avg + ')' })

        }
    }
}
