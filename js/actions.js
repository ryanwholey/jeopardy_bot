var api = api || require('./api');
var utils = utils || require('./utils');

module.exports = (function() {

    return {

        fireGetQuestion: function (options, params, callback) {
            var channel = options.channelName,
                userName = options.userName,
                errorMessage = 'Error fetching question';

            api.getRandomQuestion(userName)
                .then(utils.setQuestionAsked.bind(this, callback, options, params))
                .then(utils.formatQuestion)
                .then(utils.sendMessage.bind(this, channel, params))
                .catch(utils.handleError.bind(this, errorMessage));
        },

        fireGetScores(options, params) {
            var channel = options.channelName,
                errorMessage = 'Error fetching scores';

            api.getScores()
                .then(utils.formatScores)
                .then(utils.sendMessage.bind(this, channel, params))
                .catch(utils.handleError.bind(this, errorMessage));
        },

        fireMidQuestion(options, params) {
            var channel = options.channelName,
                midQuestionMessage = 'Another question is currently on the table',
                errorMessage = 'Error sending mid question response';

            try {
                utils.sendMessage.call(this, channel, params, midQuestionMessage);
            } catch (error) {
                utils.handleError(errorMessage, error);
            }
        },

        fireUnsetQuestion(options, params) {
            var channel = options.channelName;
            var customMessage = this.config.timesUpMessages[Math.random() * 4 | 0];
            var answer = utils.formatAnswerText(this.state.question.answer);
            var expiredMessage = ':alarm_clock:  ' + customMessage + '`'+ answer +'`'+ ' :alarm_clock:';
            utils.sendMessage.call(this, channel, params, expiredMessage);
            this.state.question = null;
            clearTimeout(this.timeout);
        },

        fireAnswer(options, params) {
            var question = this.state.question;

            if (!question) {
                utils.handleError('No question error: question is false', new Error());
                return;
            }

            var questionAnswer = question.answer.split(' ');
            var userAnswer = utils.extractAnswer(options.msgArray);
            var isCorrect = utils.validateAnswer.apply(this, [userAnswer, questionAnswer].map(utils.cleanAnswer));

            options.handleAnswerWithType(options, params, isCorrect);

            if (isCorrect) {
                options.handleUnsetQuestion();
            }
        },

        fireAnswerNoQuestion(options, params) {
            var channel = options.channelName,
                question = this.state.question,
                noQuestionMessage = 'Sorry, the question has expired, ask another with `!trabek question`',
                helpMenuMessage = 'See a list of commands with `!trabek help`';

            if (question) {
                utils.handleError('No question error: question is true', new Error());
            }

            var message = [noQuestionMessage, helpMenuMessage].join('\n');
            utils.sendMessage.call(this, channel, params, message);
        },

        fireMenu(options, params) {
            var channel = options.channelName,
                commands = options.menu;

            var msg = [];
            msg.push('*~ MENU ~*');
            msg.push('Talk to Trabek by using `!trabek <command> {<options>}`');
            for (command in commands) {
                if (commands.hasOwnProperty(command)) {
                    var line = '\t• \`' + command + '\`' + '\t' + commands[command];
                    msg.push(line);
                }
            }
            msg.push('`!buzz <answer>` will also fire an answer to Trabek');
            msg.push(' - Participants will have ' + this.config.questionTime + ' seconds to `buzz` in and answer.');
            msg.push(' - Answers must be formatted in the format of a question');
            msg.push(' - Be nice to Trabek Bot or you\'ll have to make amends to him');
            message = msg.join('\n');
            utils.sendMessage.call(this, channel, params, message);
        },

        fireAnswerWithType(options, params, isCorrect) {
            var channel = options.channelName,
                userName = options.userName,
                question = this.state.question,
                errorMessage = 'fireCorrect: no question found';

            if (!question) {
                utils.handleError(errorMessage, new Error());
            }

            options.correct = isCorrect;

            api.patchAnsweredQuestion(userName, question.id, isCorrect)
                .then(utils.formatAnswerResponse.bind(this, options))
                .then(utils.sendMessage.bind(this, channel, params))
                .catch(utils.handleError.bind(this, errorMessage));

        }
    };
})();