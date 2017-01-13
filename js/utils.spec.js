var utils = require('./utils');

describe('Utils', function() {

    describe('cleanAnswer', function() {

        it('should clean out commas quotes, commas and periods', function() {
            var actual= utils.cleanAnswer(',./;\':\"?!><');
            var expected = [];

            expect(actual).toEqual(expected);
        });

        it('should clean out & symbols', function() {
            var questionAnswer = ['Jack', '&', 'Jill'];
            var expected = ['jack', 'jill'];

            expect(utils.cleanAnswer(questionAnswer)).toEqual(expected);
        });
    });

    describe('validateAnswer', function() {

        it('should return true with correct answer', function() {
            expect(utils.validateAnswer('i am obama!', 'i am obama!')).toEqual(false);
        });

        it('should return true "how stella got her groove back"', function() {
            var questionAnswer = [ 'how', 'stella', 'got', 'her', 'groove', 'back' ];
            var userAnswer = [ 'how', 'stella', 'got', 'her', 'groove', 'back' ];

            expect(utils.validateAnswer(userAnswer, questionAnswer)).toEqual(true);
        });

        it('should return true "20 cents 4 times"', function() {
            var questionAnswer = [ '20', 'cents', '4', 'times'];
            var userAnswer = [ 'what', 'is', '20', 'cents', '4', 'times' ];

            expect(utils.validateAnswer(userAnswer, questionAnswer)).toEqual(true);
        });

        it('should return true "a horn"', function() {
            var questionAnswer = ['a', 'horn'];
            var userAnswer = ['what', 'horn'];

            expect(utils.validateAnswer(userAnswer, questionAnswer)).toEqual(true);
        });

        it('should return true "Jack & Jill"', function () {
            var questionAnswer = ['Jack', 'Jill'];
            var userAnswer = ['who', 'Jack', 'and', 'Jill'];

            expect(utils.validateAnswer(userAnswer, questionAnswer)).toEqual(true);
        });
    });

    describe('clean and validate', function() {

        it('should return true "Schindler\'s List"', function() {
            var questionAnswer = "Schindler's List".split(' ');
            var userAnswer = "what is Schindlers list".split(' ');
            var isCorrect = utils.validateAnswer.apply(this, [userAnswer, questionAnswer].map(utils.cleanAnswer));

            expect(isCorrect).toEqual(true);
        });

        it('should return false "Schindler\'s List"', function() {
            var questionAnswer = "Schindler's List".split(' ');
            var userAnswer = "what is Schindlers".split(' ');
            var isCorrect = utils.validateAnswer.apply(this, [userAnswer, questionAnswer].map(utils.cleanAnswer));

            expect(isCorrect).toEqual(false);
        });

        it('should return false "Schindler\'s List"', function() {
            var questionAnswer = "Schindler's List".split(' ');
            var userAnswer = "how is schindler's list".split(' ');
            var isCorrect = utils.validateAnswer.apply(this, [userAnswer, questionAnswer].map(utils.cleanAnswer));

            expect(isCorrect).toEqual(true);
        });

        it('should return true "Jack & Jill"', function() {
            var questionAnswer = "Jack & Jill".split(' ');
            var userAnswer = "Who are jack and jill".split(' ');
            var isCorrect = utils.validateAnswer.apply(this, [userAnswer, questionAnswer].map(utils.cleanAnswer));

            expect(isCorrect).toEqual(true);
        });

        it('should return true "(John) Newman"', function() {
            var questionAnswer = "(John) Newman".split(' ');
            var userAnswer = "what is the newman award".split(' ');
            var isCorrect = utils.validateAnswer.apply(this, [userAnswer, questionAnswer].map(utils.cleanAnswer));

            expect(isCorrect).toEqual(true);
        });
    });

    describe('clean', function() {
        it('should return correct for "Haight-Ashbury"', function() {
            var questionAnswer= "Haight-Ashbury";
            var expected = ['haight', 'ashbury'];
            var actual = utils.cleanAnswer(questionAnswer);

            expect(actual).toEqual(expected);
        });
    });
});

