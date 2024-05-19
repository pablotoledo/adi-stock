import logging

def setup_logger(name='financials_logger', level=logging.INFO):
    """
    Configura y retorna un logger.
    
    Args:
        name (str): Nombre del logger.
        level (int): Nivel del logger (por defecto es logging.INFO).
    
    Returns:
        logging.Logger: Logger configurado.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Crear un handler para la consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Crear un formato para los mensajes de log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # Añadir el handler al logger
    if not logger.handlers:
        logger.addHandler(console_handler)
    
    return logger
