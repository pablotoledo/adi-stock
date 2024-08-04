import logging

def setup_logger():
    logger = logging.getLogger('financial_data_analyzer')
    logger.setLevel(logging.DEBUG)

    # Crear un manejador de archivo
    file_handler = logging.FileHandler('financial_data_analyzer.log')
    file_handler.setLevel(logging.DEBUG)

    # Crear un manejador de consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Crear un formateador
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Agregar los manejadores al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()