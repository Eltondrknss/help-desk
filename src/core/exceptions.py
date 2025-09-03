class ApplicationError(Exception):
    #excessao base pra todos os erros
    pass

class ValidationError(ApplicationError):
    #erro na validacao dos dados de entrada
    pass

class ResourceNotFoundError(ApplicationError):
    #quando um recurso nao e encontrado (usuario, chamado...)
    pass

class InvalidStateError(ApplicationError):
    #quando a operacao nao ee possivel no estado atual
    pass

class AuthenticationError(ApplicationError):
    #pra falha de autenticacao
    pass

class PermissionDeniedError(ApplicationError):
    #pra falha por falta de permissao
    pass