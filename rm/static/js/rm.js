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

        init_focus: function(){
            $('.item.active input').focus();
        },

        init_enter_sliding: function(){
            $(document).on('keypress', '.item.active input',
                           function(e){
                               console.log(e)
                               if (e.which == 13) {
                                   $(".carousel-control.right").click()
                                   return false;
                               }
                           });
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
                    }else if(src.attr('value') == 'da' ){
                        hidem();
                        showem('#instruction-date-container');
                    }else{
                        hidem();
                    }
                }
            )

            $('input[name="reporting_style"]').change(
                function(e){
                    var hidem = function(){
                        $('#reporting-freq-container').hide();
                        $('#reporting-date-container').hide();
                    }
                    var showem = function(sel){$(sel).show()}

                    console.log(e)
                    var src = $(e.target);
                    hidem();
                    if(src.attr('value') == 're'){
                        showem('#reporting-freq-container');
                    }else if(src.attr('value') == 'da'){
                        showem('#reporting-date-container')
                    }
                }
            )


            $('input[name="ending_style"]').change(
                function(e){
                    var hidem = function(){
                        $('#ending-reports-container').hide();
                        $('#ending-date-container').hide();
                    }
                    var showem = function(sel){$(sel).show()}

                    console.log(e)
                    var src = $(e.target);
                    hidem();
                    if(src.attr('value') == 're'){
                        showem('#ending-reports-container');
                    }else if(src.attr('value') == 'da'){
                        showem('#ending-date-container')
                    }
                }
            )


        },

        init_modalinvite: function(){
            $('form#invite-form').ajaxForm({

                beforeSubmit: function(){
                    $('#btn-invite').attr('disabled', true)
                },

                success: function(data){
                    $('#btn-invite').attr('disabled', false)
                    console.log('ta!');
                    var email_input = $('#invite-form input:visible');
                    var invited = email_input.attr('value');
                    email_input.attr('value', '');
                    $('#invited-list').append('<li>'+invited+'</li>');
                },

                error: function(data){
                    console.log('nah!')
                    $('#btn-invite').attr('disabled', false)
                },

            })
        },

        // Bind the power calculation form to an ajax call
        init_power: function(options){
            var n1trial = options.n1trial;
            if(n1trial){
                var varname = 'observations';
                var target_input = '#id_ending_reports'
            }else{
                var varname = 'participants';
                var target_input = '#id_min_participants';
            }
            $('form#power-form').ajaxForm({

                beforeSubmit: function(){
                    if(!$('form#power-form').parsley().validate()){
                        return false
                    }
                    $('#power-btn').attr('disabled', true).text(
                        'calculating required ' + varname + '...')
                },

                success: function(data){
                    var msg = 'You need ' + data + ' ' + varname;
                    $('#power-btn').attr('disabled', false).text(
                    'run the numbers');
                    $('#power-answer').text(msg).addClass('active');
                    $(target_input).attr('value', data);
                    $('#power-done').text('done')
                },

                error: function(data){
                    console.log(data);
                    console.log('Power calculation - something went wrong :()')
                    $('#power-btn').attr('disabled', false).text(
                    'run the numbers');
                },

            })

            $('a#power-guestimate').on('click', function(){
                var form = $('form#power-form')
                $('form#power-form input#power').attr('value', '0.8');
                $('form#power-form input#alpha').attr('value', '0.05');
                $('form#power-form input#effect-size').attr('value', '0.5');
                form.submit()
                return false;
            })

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
    },

    interactions: {

        report_template: _.template('<tr><td>*</td><td><%=group_name %></td><td><a href="#report-data" class="btn btn-danger" data-toggle="modal" role="button">report data</a></td></tr>'),

        // Initialise the randomisation functionality for n=1 trials.
        randomise_me: function(){

            // The randomise me button itself
            $('#randomiseme-form').ajaxForm({
                success: function(data){
                    var instructions = $('#group' + data + '-instructions').text();
                    if(data == 'a'){
                        var group_name = 'Group A';
                    }else{
                        var group_name = 'Group B';
                    }
                    $('#active-instructions').text(instructions);
                    $('#instruction-container').slideDown();
                    $('#randomiseme-button').slideToggle();
                    var row = RM.interactions.report_template({group_name:group_name})
                    $('#report-table table').append(row);
                    if(!$('#report-table').is(':visible')){
                        $('#report-table').slideDown()
                    }
                }
            });

        },

        // Make sure that nof1 report forms validate please.
        nof1_reporting: function(){

            // Handle enter in the form
            $(document).on('keypress', '.ajaxform:visible',
                           function(e){
                               if (e.which == 13) {
                                   $("form.ajaxform:visible").submit();
                                   return false;
                               }
                               return true;
                           });

            $('form.ajaxform').on('submit', function(){
                return $('form.ajaxform:visible').parsley('validate');
            });
        },

        // Toggle slide up/down on dashboard-style widgets
        dashboard_expand: function(){
            $('a.expand').on('click', function(e){
                window.console.log(e)
                var target = $(e.target);
                window.console.log(target);
                target.parent().parent().children('.dashboard-widget-body').children('.dashboard-widget-extra').slideToggle()
                if(target.attr('data-wastext')){
                    target.text(target.attr('data-wastext')).attr('data-wastext', null);
                }else{
                    target.attr('data-wastext', target.text()).text('hide most');
                }
                return false;
            })
        },

    }

}
