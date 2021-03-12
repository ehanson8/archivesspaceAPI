import csv
import json
import logging


from asaps import workflows


def test_create_new_dig_objs(as_ops, caplog, runner):
    """Test create_new_dig_objs method."""
    caplog.set_level(logging.INFO)
    with runner.isolated_filesystem():
        with open('metadata.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['uri'] + ['link'])
            writer.writerow(['/repositories/0/archival_objects/1234'] +
                            ['mock://example.com/handle/111.1111'])
        workflows.create_new_dig_objs(as_ops, 'metadata.csv', '0')
        message_1 = json.loads(caplog.messages[1])['event']
        message_2 = json.loads(caplog.messages[2])['event']
        assert message_1['uri'] == '/repositories/0/digital_objects/5678'
        assert message_2['post'] == 'Success'


def test_export_metadata(as_ops):
    """Test export_metadata method."""
    report_dicts = workflows.export_metadata(as_ops, '423', 'ref_id', '0')
    for report_dict in report_dicts:
        assert report_dict['uri'] == '/repositories/0/archival_objects/1234'
        assert report_dict['title'] == 'Sample Title'
        assert report_dict['file_identifier'] == 'a2b2c2'