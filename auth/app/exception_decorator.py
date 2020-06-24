from logger import logger
import traceback


def exit_exception():
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur

    @param logger: The logging object
    """

    def decorator(func):

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error("There was an exception in {func}"
                             .format(func=func.__name__))
                failed_func = str(args[0]).split()
                failed_func[1] = failed_func[1].strip("()")
                logger.error("failed_func=[{func}]".format(func=failed_func))
                logger.error("{err}\n{trace}"
                             .format(err=e, trace=traceback.format_exc()))
                raise SystemExit

        return wrapper
    return decorator
