import unittest
from Tokenizer import Tokenizer
from Parser import Parser, makeTree
from Productions import assign_stmt, vardec_stmt, while_stmt, if_stmt, return_stmt

class AST_tester(unittest.TestCase):

    def test_full_program_ast_tree(self):
        source = '''
            class Animal {
                Int age;
                Boolean isAlive;
                Int nameId;
                
                init() {
                    super();
                    this.age = 0;
                    this.isAlive = true;
                    this.nameId = 0;
                }
                
                method speak() Void {
                    return println(this.nameId);
                }
                
                method getAge() Int {
                    return this.age;
                }
                
                method setAge(Int newAge) Void {
                    this.age = newAge;
                }
            }
            
            class Dog extends Animal {
                Int barkCount;
                Boolean isGoodBoy;
                
                init() {
                    super();
                    this.barkCount = 0;
                    this.isGoodBoy = true;
                }
                
                method speak() Void {
                    this.barkCount = this.barkCount + 1;
                    if (this.isGoodBoy) {
                        return println(1);
                    } else {
                        return println(0);
                    }
                }
                
                method getBarkCount() Int {
                    return this.barkCount;
                }
            }
            
            Animal pet;
            Dog myDog;
            Int count;
            Boolean isFirst;
            
            myDog = new Dog();
            pet = myDog;
            count = 0;
            isFirst = true;
            
            while (count < 3) {
                if (isFirst) {
                    pet.speak();
                    isFirst = false;
                } else {
                    myDog.speak();
                }
                count = count + 1;
            }
            
            if (myDog.getBarkCount() > 0) {
                println(myDog.getAge());
            } else {
                println(0);
            }
            
            return 0;
            '''
        tokenizer = Tokenizer(source)
        tokens = tokenizer.read_Tokens()
        parser = Parser(tokens)
        program = parser.program().result
        
        tree = makeTree(program)
        print("\nFull Program AST:")
        print(tree.to_string())
        
        # Verify the AST structure
        self.assertEqual(len(program.classes), 2)
        self.assertEqual(program.classes[0].class_name, "Animal")
        self.assertEqual(program.classes[1].class_name, "Dog")
        self.assertEqual(program.classes[1].extends_name, "Animal")
        
        # Verify statements
        self.assertEqual(len(program.stmts), 11)  # 4 declarations, 4 assignments, 1 while, 1 if, 1 return
        
        # Verify statement types
        self.assertTrue(isinstance(program.stmts[0], vardec_stmt))  # Animal pet
        self.assertTrue(isinstance(program.stmts[1], vardec_stmt))  # Dog myDog
        self.assertTrue(isinstance(program.stmts[2], vardec_stmt))  # Int count
        self.assertTrue(isinstance(program.stmts[3], vardec_stmt))  # Boolean isFirst
        self.assertTrue(isinstance(program.stmts[4], assign_stmt))  # myDog = new Dog()
        self.assertTrue(isinstance(program.stmts[5], assign_stmt))  # pet = myDog
        self.assertTrue(isinstance(program.stmts[6], assign_stmt))  # count = 0
        self.assertTrue(isinstance(program.stmts[7], assign_stmt))  # isFirst = true
        self.assertTrue(isinstance(program.stmts[8], while_stmt))   # while loop
        self.assertTrue(isinstance(program.stmts[9], if_stmt))      # if statement
        self.assertTrue(isinstance(program.stmts[10], return_stmt)) # return 0

if __name__ == '__main__':
    unittest.main()
