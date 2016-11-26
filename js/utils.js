module.exports = (function() {

    var validQuestionWords = {
        who: 'who',
        whos: 'whos',
        what: 'what',
        whats: 'whats',
        when: 'when',
        whens: 'whens',
        where: 'where',
        wheres: 'wheres',
        why: 'why',
        whys: 'whys',
        how: 'how',
        hows: 'hows',
    };

    var wordsToOverlook = {
        a: 'a',
        the: 'the'
    };

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
            var formatted = scores
                .sort(function(a, b) {
                    return a.score < b.score;
                })
                .map(function(score, index) {
                    return (index + 1) + ') ' + score.name + ': ' + score.score;
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
        },

        extractAnswer: function(msgArray) {
            var slicer = msgArray[0] === '!trabek' ? 2 : 1;

            return msgArray.slice(slicer);
        },

        cleanAnswer: function(answerArray) {
            if (!Array.isArray(answerArray)) {
                answerArray = answerArray.split(' ');
            }

            var answer = answerArray
                .map(function(word) {
                    return unescape(word).replace(/[\'|\"|\.|\,|\/|\\|&|?|!|>|<|/{|/}|/(|/)|/:|/;]/g, '').toLowerCase();
                }).filter(function(word) {
                    return !!word;
                });

            return answer;
        },

        validateAnswer: function(userAnswer, questionAnswer) {
            if (!validQuestionWords[userAnswer[0]]) {
                return false;
            }
            return questionAnswer.reduce(function(memo, word) {
                if (!memo) {
                    return false;
                } else if (wordsToOverlook[word]) {
                    return true;
                } else {
                    return userAnswer.indexOf(word) >= 0;
                }
            }, true);
        },

        formatAnswerResponse: function(options, player) {
            var msg = [];

            if (options.correct) {
                msg.push('Correct ' + player.name + '!');
            } else {
                msg.push('Sorry, ' + player.name + ', incorrect...');
            }
            msg.push(' - _Updated score_ -');
            msg.push(player.name + ': $' + player.score);

            return msg.join('\n');
        }
    };

})();