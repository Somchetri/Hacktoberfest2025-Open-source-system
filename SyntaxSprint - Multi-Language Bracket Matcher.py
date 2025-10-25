class BracketMatcher:
    def __init__(self):
        self.pairs = {
            '(': ')',
            '[': ']',
            '{': '}',
            '<': '>'
        }
        self.opening = set(self.pairs.keys())
        self.closing = set(self.pairs.values())
    
    def validate(self, code):
        """Validate bracket matching in code"""
        stack = []
        errors = []
        
        for line_num, line in enumerate(code.split('\n'), 1):
            # Skip comments (basic detection)
            if line.strip().startswith(('//','#')):
                continue
            
            for col_num, char in enumerate(line, 1):
                if char in self.opening:
                    stack.append({
                        'char': char,
                        'line': line_num,
                        'col': col_num
                    })
                elif char in self.closing:
                    if not stack:
                        errors.append({
                            'type': 'UNMATCHED_CLOSING',
                            'char': char,
                            'line': line_num,
                            'col': col_num,
                            'message': f'Unmatched closing bracket "{char}"'
                        })
                    else:
                        last_opening = stack.pop()
                        expected = self.pairs[last_opening['char']]
                        if char != expected:
                            errors.append({
                                'type': 'MISMATCHED',
                                'char': char,
                                'line': line_num,
                                'col': col_num,
                                'message': f'Expected "{expected}" but found "{char}"',
                                'opening_line': last_opening['line']
                            })
        
        # Check for unclosed brackets
        for unclosed in stack:
            errors.append({
                'type': 'UNCLOSED',
                'char': unclosed['char'],
                'line': unclosed['line'],
                'col': unclosed['col'],
                'message': f'Unclosed bracket "{unclosed["char"]}"'
            })
        
        return errors
    
    def display_results(self, errors):
        """Display validation results"""
        if not errors:
            print("✅ All brackets are properly matched!")
            return
        
        print(f"\n❌ Found {len(errors)} bracket matching error(s):\n")
        for error in errors:
            print(f"Line {error['line']}, Column {error['col']}: {error['message']}")
            if error['type'] == 'MISMATCHED' and 'opening_line' in error:
                print(f"   (Opening bracket was on line {error['opening_line']})")
            print()

# Usage
matcher = BracketMatcher()

test_code = """
def calculate(a, b):
    result = (a + b) * 2
    if result > 10:
        print("Result is {result}")
        return result
    ]
    return 0
"""

errors = matcher.validate(test_code)
matcher.display_results(errors)

# Test with valid code
valid_code = """
function process() {
    let data = [1, 2, 3];
    return data.map(x => x * 2);
}
"""

print("\nTesting valid code:")
errors2 = matcher.validate(valid_code)
matcher.display_results(errors2)
