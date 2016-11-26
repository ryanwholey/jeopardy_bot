module.exports = (function() {

    var $ = require('request-promise');
    var utils = require('./utils');

    var user = process.env.JEOPARDY_USERNAME;
    var pass = process.env.JEOPARDY_PASSWORD;
    var host = process.env.JEOPARDY_HOST || 'http://' + user + ':' + pass + '@localhost';
    var port = process.env.JEOPARDY_PORT || 8000;
    var base_url = host + ':' + port + '/api/';

    if (!user || !pass) {
        throw new Error('Please set your username and password or the api wont work');
    }

    return {

        getRandomQuestion: function(userName) {
            var url = base_url + 'questions/random/';
            var errorMessage = 'API Error: fetch question error';

            options = {
                method: 'POST',
                uri: url,
                body: {
                    player: userName
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
                    console.log(question)
                    return question;
                })
                .catch(utils.handleError.bind(this, errorMessage));

        },

        getScores: function() {
            var url = base_url + 'players/';
            var errorMessage = 'API Error: Error fetching scores';

            return $(url)
                .then(function(response) {
                    var scores = JSON.parse(response);
                    return scores;
                })
                .catch(utils.handleError.bind(this, errorMessage));

        },

        patchAnsweredQuestion: function(userName, questionId, isCorrect) {
            var answerType = isCorrect ? 'correct' : 'incorrect',
                url = base_url + 'players/name/' + userName + '/?' + answerType + '=' + questionId,
                errorMessage = 'Error patching correct question to ' + userName + ' with qid ' + questionId;

            var options = {
                method: 'PATCH',
                uri: url
            };

            return $(options)
                .then(function(response) {
                    return JSON.parse(response);
                })
                .catch(utils.handleError.bind(this, errorMessage));
        }
    };

})();
