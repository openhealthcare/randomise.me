// Main Randomise.me Javascript file.
//

var RM = {
    graphs: {
        single_user_trial: function(selector, data){
            var chart = d3.select(selector).append('svg')
                        .attr('class', 'chart')
                        .attr('width', 420)
                        .attr('height', 60 * data.length);

            var x = d3.scale.linear()
                    .domain([0, d3.max(_.pluck(data, 'avg'))])
                    .range([0, 420]);

            // var y = d3.scale.ordinal()
            //     .domain(_.pluck(data, 'name'))
            //     .rangeBands([0, 120]);

            chart.selectAll('rect')
                .data(data)
                .enter().append('rect')
            .attr('y', function(d, i){ return i * 60; })
            .attr('width', function(d) { return x(d.avg)})
            .attr('height', 60)

            chart.selectAll('text')
                .data(data)
                .enter().append('text')
                .attr('x', function(d) { return x(d.avg); })
                .attr('y', function(d, i) { return i * 60 + 60 / 2 })
                .attr('dx', -3)
                .attr('dy', '.35em')
                .attr('text-anchor', 'end')
                .text(function(d) { return d.name + ' (' + d.avg + ')' })

        }
    }
}
