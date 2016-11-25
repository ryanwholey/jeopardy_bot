module.exports = (function() {

    return {
        formatQuestion: function(question) {
            var msg = [];

            msg.push('Category: ' + question.category);
            msg.push('For $' + question.value);
            msg.push(question.question);

            return msg.join('\n');
        },

        formatScores: function(scores) {
            var msg = [];

            msg.push('*SCORES*');
            var formatted = scores.map(function(score) {
                return score.name + ': ' + score.score;
            });

            return msg.concat(formatted).join('\n');
        },

        sendMessage: function(channel, params, message) {
            this.postMessage(channel, message, params);
        },

        handleError: function(message, err) {
            console.log(message, err);
        },

        setQuestionAsked: function(callback, question) {
            this.state.question = question;

            this.timeout = setTimeout(callback, this.config.questionTime * 1000);

            return question;
        }
    };

})();