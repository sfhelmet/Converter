from config import DECODE_CONSTANT

def get_params(function: str) -> list[str]:
  print("f", function)
  start_bracket = function.find("(")
  end_bracket = function.rfind(")")

  if start_bracket == -1 or end_bracket == -1:
    raise Exception("Error: Invalid Parenthesis")
  
  else:
    return [param.strip() for param in function[start_bracket + 1:end_bracket].split(",")]
  
def get_function_name(function: str) -> str:
  return function[:function.find("(")]

def strip_binary(s) -> str:
  if type(s) == str:
    return s
  else:
    return s.decode(DECODE_CONSTANT)
