import sys
from parser import Parser
from environment import Environment, Builtins, Expression


class Interpreter(object):

    """This class holds references to input and output streams and
    their prompts and uses them for running a line based interpreter.

    Public methods:
    run() -- Run interpreter by evaluating expressions

    """

    def __init__(self, instream=sys.stdin, outstream=sys.stdout,
                 prompt1=None, prompt2=None):
        """Create Interpreter object.

        Keyword arguments:
        instream -- stream to read input from (default sys.stdin)
        outstream -- stream to write output to (default sys.stdout)
        prompt1 -- Normal prompt (default '> ' if interactive)
        prompt2 -- Secondary prompt (default None)

        """

        self.instream = instream
        self.outstream = outstream

        if prompt1 is None and instream.isatty() and outstream.isatty():
            prompt1 = '> '
        self.prompt1 = prompt1
        self.prompt2 = prompt2
        self.parser = Parser(self.instream, self.outstream,
                             self.prompt1, self.prompt2)
        self.environment = Environment(namespace=Builtins.namespace(outstream))

    def run(self):
        """Run interpreter by evaluating expessions.

        Parses input stream and returns expressions which then are
        evaluated by the environment.  The results are then written,
        for each evaluated expression, to the output stream.

        """

        if self.prompt1:
            self.outstream.write(self.prompt1)
        try:
            for expr in self.parser.expressions():
                result = self.environment.eval(expr)
                if result is not None:
                    print result
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    if len(sys.argv) > 1:
        for file_ in sys.argv[1:]:
            with open(file_, 'r') as f:
                Interpreter(f).run()
    else:
        Interpreter().run()
