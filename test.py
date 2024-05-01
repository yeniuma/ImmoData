import DataCleanFunc as DCF
import pandas as pd


def test_transform_raw_data_expected_cols_are_present():
    #arrange
    data = pd.DataFrame({
        'ID':['148223293']
        ,'Property_type':['Dachgeschoss']
        ,'Street':['NA']
        ,'Region_and_country':['1120 Wien, 12. Bezirk, Meidling']
        ,'Apt_size':['135,8 m²']
        ,'Floor':['4 von 5']
        ,'Move_in':['ab sofort']
        ,'Nr_of_rooms':['5']
        ,'Nr_of_bathrooms':['2']
        ,'Cold_price':['1696,28 €']
        ,'Warm_price':['~2.160 €']
        ,'Labels':['Personenaufzug,Einbauküche']
        ,'Pets_allowed':['NA']
        ,'Year_built':['1999']
        ,'Heating':['Etagenheizung']
        ,'Heating_price':['keine Angabe']
        ,'Parking':['1 Garage']
        ,'Deposit':['2900']
        ,'Status':['Gepflegt']
        ,'Desc':['Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lectus magna fringilla urna porttitor rhoncus dolor purus. Eu non diam phasellus vestibulum lorem sed risus ultricies. Rhoncus urna neque viverra justo. Id aliquet risus feugiat in ante metus dictum. Pellentesque massa placerat duis ultricies lacus sed turpis. Maecenas pharetra convallis posuere morbi leo urna molestie at elementum. Nisi vitae suscipit tellus mauris a diam maecenas sed. Amet cursus sit amet dictum sit amet justo. Lectus mauris ultrices eros in cursus. Feugiat scelerisque varius morbi enim nunc. Purus ut faucibus pulvinar elementum. Pretium vulputate sapien nec sagittis aliquam malesuada. Sit amet commodo nulla facilisi nullam vehicula ipsum a. Neque aliquam vestibulum morbi blandit. Pharetra magna ac placerat vestibulum lectus mauris. Integer feugiat scelerisque varius morbi enim nunc faucibus a. Enim nec dui nunc mattis enim ut tellus elementum.']
        ,'URL':['https://www.immobilienscout24.de/expose/148223293?referrer=RESULT_LIST_LISTING&searchId=b3d9a876-889a-3a54-adc5-1fa495cacf45&searchType=district#/']
        ,'Time':['1704223495.5336']
    })
    expected_cols = ('District','Apt_size_unit','Cold_price_unit','Cold_price_per_sqm','Cold_price_per_sqm_unit','Warm_price_unit','latitude','longitude')

    #act
    transformed_data= DCF.transform_raw_data(data)

    #assert
    for col in expected_cols:
        assert col in list(transformed_data.columns)

        
def test_transform_raw_data_check_if_split_works():
    data= pd.DataFrame({
        'ID':['148223293']
        ,'Property_type':['Dachgeschoss']
        ,'Street':['NA']
        ,'Region_and_country':['1120 Wien, 12. Bezirk, Meidling']
        ,'Apt_size':['135,8 m²']
        ,'Floor':['4 von 5']
        ,'Move_in':['ab sofort']
        ,'Nr_of_rooms':['5']
        ,'Nr_of_bathrooms':['2']
        ,'Cold_price':['1696,28 €']
        ,'Warm_price':['~2.160 €']
        ,'Labels':['Personenaufzug,Einbauküche']
        ,'Pets_allowed':['NA']
        ,'Year_built':['1999']
        ,'Heating':['Etagenheizung']
        ,'Heating_price':['keine Angabe']
        ,'Parking':['1 Garage']
        ,'Deposit':['2900']
        ,'Status':['Gepflegt']
        ,'Desc':['Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lectus magna fringilla urna porttitor rhoncus dolor purus. Eu non diam phasellus vestibulum lorem sed risus ultricies. Rhoncus urna neque viverra justo. Id aliquet risus feugiat in ante metus dictum. Pellentesque massa placerat duis ultricies lacus sed turpis. Maecenas pharetra convallis posuere morbi leo urna molestie at elementum. Nisi vitae suscipit tellus mauris a diam maecenas sed. Amet cursus sit amet dictum sit amet justo. Lectus mauris ultrices eros in cursus. Feugiat scelerisque varius morbi enim nunc. Purus ut faucibus pulvinar elementum. Pretium vulputate sapien nec sagittis aliquam malesuada. Sit amet commodo nulla facilisi nullam vehicula ipsum a. Neque aliquam vestibulum morbi blandit. Pharetra magna ac placerat vestibulum lectus mauris. Integer feugiat scelerisque varius morbi enim nunc faucibus a. Enim nec dui nunc mattis enim ut tellus elementum.']
        ,'URL':['https://www.immobilienscout24.de/expose/148223293?referrer=RESULT_LIST_LISTING&searchId=b3d9a876-889a-3a54-adc5-1fa495cacf45&searchType=district#/']
        ,'Time':['1704223495.5336']
    })

    transformed_df = DCF.transform_raw_data(data)

    assert transformed_df['Apt_size'][0] == 135.8
    assert transformed_df['Apt_size_unit'][0] == 'm²'
    assert transformed_df['Cold_price'][0] == 1696.28
    assert transformed_df['Cold_price_unit'][0] == '€'
    assert transformed_df['Warm_price'][0] == '~2.160'
    assert transformed_df['Warm_price_unit'][0] == '€'


def test_transform_raw_data_check_if_replace_works():
    data= pd.DataFrame({
        'ID':['148223293']
        ,'Property_type':['Dachgeschoss']
        ,'Street':['Am Grünen Prater,']
        ,'Region_and_country':['1120 Wien, 12. Bezirk, Meidling']
        ,'Apt_size':['135,8 m²']
        ,'Floor':['4 von 5']
        ,'Move_in':['ab sofort']
        ,'Nr_of_rooms':['5']
        ,'Nr_of_bathrooms':['2']
        ,'Cold_price':['1696,28 €']
        ,'Warm_price':['~2.160 €']
        ,'Labels':['Personenaufzug,Einbauküche']
        ,'Pets_allowed':['NA']
        ,'Year_built':['1999']
        ,'Heating':['Etagenheizung']
        ,'Heating_price':['keine Angabe']
        ,'Parking':['1 Garage']
        ,'Deposit':['2900']
        ,'Status':['Gepflegt']
        ,'Desc':['Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lectus magna fringilla urna porttitor rhoncus dolor purus. Eu non diam phasellus vestibulum lorem sed risus ultricies. Rhoncus urna neque viverra justo. Id aliquet risus feugiat in ante metus dictum. Pellentesque massa placerat duis ultricies lacus sed turpis. Maecenas pharetra convallis posuere morbi leo urna molestie at elementum. Nisi vitae suscipit tellus mauris a diam maecenas sed. Amet cursus sit amet dictum sit amet justo. Lectus mauris ultrices eros in cursus. Feugiat scelerisque varius morbi enim nunc. Purus ut faucibus pulvinar elementum. Pretium vulputate sapien nec sagittis aliquam malesuada. Sit amet commodo nulla facilisi nullam vehicula ipsum a. Neque aliquam vestibulum morbi blandit. Pharetra magna ac placerat vestibulum lectus mauris. Integer feugiat scelerisque varius morbi enim nunc faucibus a. Enim nec dui nunc mattis enim ut tellus elementum.']
        ,'URL':['https://www.immobilienscout24.de/expose/148223293?referrer=RESULT_LIST_LISTING&searchId=b3d9a876-889a-3a54-adc5-1fa495cacf45&searchType=district#/']
        ,'Time':['1704223495.5336']
    })

    transformed_df = DCF.transform_raw_data(data)

    assert transformed_df['Apt_size'][0] == 135.8
    assert transformed_df['Cold_price'][0] == 1696.28
    assert transformed_df['Street'][0] == 'Am Grünen Prater'
