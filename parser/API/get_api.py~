import requests
import logging
from celery import shared_task

from models import LegalCategory, Document
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)

@shared_task
def parse_document_types(parent_code=None):
    categories = LegalCategory.objects.exclude(type_id__isnull=True)

    for category in categories:
        # 2. Запрашиваем документы для категории
        url = f'http://publication.pravo.gov.ru/api/Documents?block={category.block}&DocumentTypes={category.type_id}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            documents = response.json()

            for doc in documents:
                # 3. Пропускаем ненужные документы
                if 'О внесении изменений' in doc.get('name', ''):
                    continue

                # 4. Скачиваем PDF
                eoNumber = doc['eoNumber']
                pdf_url = f'http://publication.pravo.gov.ru/file/pdf?eoNumber={eoNumber}'
                pdf_response = requests.get(pdf_url, stream=True)
                pdf_response.raise_for_status()

                # 5. Сохраняем в модель Document
                pdf_name = f'document_{eoNumber}.pdf'
                document, created = Document.objects.update_or_create(
                    eoNumber=eoNumber,
                    defaults={
                        'category': category,
                        'pdf_file': ContentFile(pdf_response.content, name=pdf_name)
                    }
                )

        except Exception as e:
            logger.error(f"Ошибка при парсинге документов для категории {category.name}: {e}")

@shared_task
def parse_categories(parent_code=None):
    url = 'http://publication.pravo.gov.ru/api/PublicBlocks/'
    if parent_code:
        url += f'?parent={parent_code}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        blocks = response.json()
    except Exception as e:
        logger.error(f"Error: {e}")
        return

    for block in blocks:
        category, created = LegalCategory.objects.update_or_create(
            block=block['code'],
            defaults={'name': block['name'], 'auto_updates': True}
        )

        parse_categories.delay(block['code'])

        if not block.get('has_children'):
            parse_document_types.delay(block['code'])