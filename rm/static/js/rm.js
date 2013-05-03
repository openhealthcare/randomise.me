// Main Randomise.me Javascript file.
//

var RM = {
    graphs: {
        single_user_trial: function(selector, data){
            RM.graphs.trial_bar(selector, data, 420, 60)
            },

        trial_thumbnail: function(selector, data){
            RM.graphs.trial_bar(selector, data, 210, 30)
        },

        trial_report: function(pk, results){
            var bar_selector = "#mainbar-"+ pk;
            RM.graphs.trial_bar(bar_selector, results, 420, 60)
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
