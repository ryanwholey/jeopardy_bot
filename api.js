module.exports = (function() {

    var $ = require('request-promise');
    var utils = require('./utils');

    var user = process.env.JEOPARDY_USERNAME;
    var pass = process.env.JEOPARDY_PASSWORD;
    var host = process.env.JEOPARDY_HOST || 'http://' + user + ':' + pass + '@localhost';
    var port = process.env.JEOPARDY_PORT || 8000;
    var base_url = host + ':' + port + '/api/';

    return {

        getRandomQuestion: function(jeopardy_username) {
            var url = base_url + 'questions/random/';
            var errorMessage = 'API Error: fetch question error';

            options = {
                method: 'POST',
                uri: url,
                body: {
                    player: jeopardy_username
                },
                json: true
            };

            return $(options)
                .then(function(question) {
                    question.question = unescape(question.question);
                    // if theres an link, move it out of tags so slack can read it
                    if (question.question.indexOf('<a href=')) {
                        q = question.question;
                        question.question = q.replace(/<a.*">/, '').replace(/<\/a>/, '');
                        link = q.substr(q.indexOf('http'));
                        link = link.substr(0, link.indexOf('\"'));
                        question.question += ' ' + link;
                    }
                    return question;
                })
                .catch(utils.handleError.bind(this, errorMessage));

        },

        getScores() {
            var url = base_url + 'players/';
            var errorMessage = 'API Error: Error fetching scores';

            return $(url)
                .then(function(response) {
                    var scores = JSON.parse(response);
                    return scores;
                })
                .catch(utils.handleError.bind(this, errorMessage));

        }
    };

})();
