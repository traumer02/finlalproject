import json
from typing import List

import requests
from bs4 import BeautifulSoup

from config import Config
from models import MainInfo, Complaint, Result
from utils import logger
from services import DB, Model


class Error(Exception):
    pass


class Crawler:

    def __init__(self):
        self.soup = None
        self.fullname = None
        self.db = DB()

    @staticmethod
    def make_request(search_name: str = None, url: str = None):
        if search_name:
            params = {'q': search_name}
            try:
                logger.info('Requesting: https://projects.propublica.org/nypd-ccrb/search')
                response = requests.get(url=Config.BASE_URL + '/nypd-ccrb/search', params=params,
                                        headers=Config.headers)
                if response.ok:
                    return response.text
            except Exception as e:
                logger(f'Error while requesting {url}: {e}')
                raise Error(e)
        logger.info(f'Requesting: {url}')
        try:
            response = requests.get(url, headers=Config.headers, timeout=20)
            if response.ok:
                return response.text
        except Exception as e:
            logger.info(f'Error in request: {url}: {e}')
            raise Error(e)


    @staticmethod
    def make_soup(html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    @staticmethod
    def get_complaints(soup: BeautifulSoup):
        search_results = []
        div = soup.find('div', class_='pr3-ns pt3 w-70-l w-100')
        all_people = div.find('ul').find_all('li')
        for item in all_people:
            link = item.find('a')['href']
            search_results.append(Config.BASE_URL + link)
        return search_results

    def get_fullname(self, soup: BeautifulSoup):
        main_div = soup.find('main', class_='main-officer')
        div = main_div.find('div', class_='pg-main newsapp')
        div = div.find('div', class_='flex flex-wrap w-100 pb3')
        div = div.find('div', class_='mw7')
        full_name = div.find_all('div', class_='fw7 f2-l f4-m f5 lh-title tiempos-text')[0].text.strip()
        self.fullname = full_name
        return full_name

    @staticmethod
    def get_rank(soup: BeautifulSoup):
        main_div = soup.find('main', class_='main-officer')
        div = main_div.find('div', class_='pg-main newsapp')
        div = div.find('div', class_='flex flex-wrap w-100 pb3')
        rank = div.find('div', class_='mw7').find('div', class_='fw5 f4-l f5-m f5 lh-title tiempos-text').text.strip()

        return rank

    @staticmethod
    def get_appearance(soup: BeautifulSoup):
        main_div = soup.find('main', class_='main-officer')
        div = main_div.find('div', class_='pg-main newsapp')
        div = div.find('div', class_='flex flex-wrap w-100 pb3')
        appearance = div.find('div', class_='mw7').find_all('div', class_='fw5 f4-l f5-m f5 lh-title tiempos-text')[
            1].text.strip()
        return appearance

    @staticmethod
    def get_precinct(soup: BeautifulSoup):
        try:
            full_info = soup.find("div", class_="fw5 f4-l f5-m f5 lh-title tiempos-text")
            a = full_info.find('a')
            precinct = a.text
            return precinct  # todo: some has precinct, but others do not
        except Exception as e:
            return None

    @staticmethod
    def get_units(soup: BeautifulSoup) -> List:
        units = []
        all_units = soup.find("div", class_="f4-l f5 lh-title tiempos-text").text.strip().replace('\n', '')
        units.append(all_units)
        return units

    @staticmethod
    def get_number_of_complaints(soup: BeautifulSoup):
        all_divs = soup.find_all("div", class_="f4-l f5 lh-title tiempos-text")
        total_complaints = all_divs[1].text.strip()
        res = int(total_complaints)
        return res

    @staticmethod
    def get_number_of_allegations(soup: BeautifulSoup):
        all_divs = soup.find_all("div", class_="f4-l f5 lh-title tiempos-text")
        total_allegations = all_divs[2].text.strip()
        res = int(total_allegations)
        return res

    @staticmethod
    def get_number_of_substantiated_allegations(soup: BeautifulSoup):
        all_divs = soup.find_all("div", class_="f4-l f5 lh-title tiempos-text")
        total_substantiated_allegations = all_divs[3].text.strip()
        res = int(total_substantiated_allegations)
        return res

    @staticmethod
    def get_more_details(soup: BeautifulSoup) -> list:
        more_details = []
        elements = soup.find_all("div", class_="mb5")
        for element in elements:
            a = element.find("a")
            url_of_element = a.get("href")
            more_details.append(url_of_element)
        return more_details

    @staticmethod
    def get_date_of_complaint(soup: BeautifulSoup):
        content = soup.find("div", class_="fw7 f2-l f4-m f5 lh-title tiempos-text").text.strip()
        date_of_complaint = content[22:]
        return date_of_complaint

    @staticmethod
    def get_rank_at_time(soup: BeautifulSoup):
        content = soup.find("table", class_="table medium tablesaw-stack f6").find("tbody")
        rows = content.find_all("tr")
        for row in rows:
            content = row.text
            all_row = content.splitlines()
            rank_at_the_time = all_row[2].strip()
            return rank_at_the_time

    @staticmethod
    def get_info_about_officer(soup: BeautifulSoup):
        content = soup.find("table", class_="table medium tablesaw-stack f6").find("tbody")
        rows = content.find_all("tr")
        for row in rows:
            content = row.text
            all_row = content.splitlines()
            info_about_officer = all_row[3].strip()
            return info_about_officer

    @staticmethod
    def get_info_about_complainant(soup: BeautifulSoup):
        content = soup.find("table", class_="table medium tablesaw-stack f6").find("tbody")
        rows = content.find_all("tr")
        for row in rows:
            content = row.text
            all_row = content.splitlines()
            info_about_complainant = all_row[4].strip()
            return info_about_complainant

    @staticmethod
    def get_allegations(soup: BeautifulSoup):
        content = soup.find("table", class_="table medium tablesaw-stack f6").find("tbody")
        rows = content.find_all("tr")
        for row in rows:
            content = row.text
            all_row = content.splitlines()
            allegations = all_row[5].strip()
            return allegations

    @staticmethod
    def get_ccrb_conclusion(soup: BeautifulSoup):
        content = soup.find("table", class_="table medium tablesaw-stack f6").find("tbody")
        rows = content.find_all("tr")
        for row in rows:
            content = row.text
            all_row = content.splitlines()
            conclusion = all_row[6].strip()
            return conclusion

    def parse_more_details(self, list_of_more_details: list):
        complaints = []
        if list_of_more_details:
            for link in list_of_more_details:
                html = self.make_request(url=Config.BASE_URL + link)
                soup = self.make_soup(html)

                content = soup.find("table", class_="table medium tablesaw-stack f6")
                content = content.find('tbody')
                rows = content.find_all("tr")

                for row in rows:
                    content = row.text
                    all_row = content.splitlines()
                    name_of_officer = all_row[1]
                    if name_of_officer == self.fullname:
                        date = self.get_date_of_complaint(soup)
                        rank_at_the_time_of_incident = self.get_rank_at_time(soup)
                        officer_details = self.get_info_about_officer(soup)
                        complainant_details = self.get_info_about_complainant(soup)
                        allegations = self.get_allegations(soup)
                        conclusion = self.get_ccrb_conclusion(soup)

                        complaint = Complaint(date=date, rank_at_time=rank_at_the_time_of_incident,
                                              officer_details=officer_details,
                                              complaint_details=complainant_details, allegations=allegations,
                                              ccrb_conclusion=conclusion).model_dump()

                        complaints.append(complaint)
        return complaints

    def get_general_info(self, complaint: str):
        html = self.make_request(url=complaint)
        soup = self.make_soup(html)
        self.soup = soup
        fullname = self.get_fullname(soup)
        rank = self.get_rank(soup)
        appearance = self.get_appearance(soup)
        precinct = self.get_precinct(soup)
        units = self.get_units(soup)
        total_complaints = self.get_number_of_complaints(soup)
        total_allegations = self.get_number_of_allegations(soup)
        total_substantiated_allegations = self.get_number_of_substantiated_allegations(soup)
        policeman = MainInfo(fullname=fullname, rank=rank, appearance=appearance, precinct=precinct, units=units,
                             total_complaints=total_complaints, total_allegations=total_allegations,
                             substantiated_allegations=total_substantiated_allegations, link=complaint).model_dump()
        check_person = self.db.session.query(Model).filter(Model.link == complaint).first()
        if not check_person:
            policeman = Model(link=complaint, rank=rank, appearance=appearance, fullname=fullname, precinct=precinct)
            try:
                self.db.session.add(policeman)
                self.db.session.commit()
            except Exception as e:
                logger.info(f'Could not add data to database: {e}')
                self.db.session.rollback()
        return policeman

    def get_detailed_info_about_complaints(self):
        more_details = self.get_more_details(self.soup)
        info_about_each_complaint = self.parse_more_details(more_details)
        return info_about_each_complaint

    @staticmethod
    def write_to_file(data):
        logger.info(f'Starting to write to file')
        with open('/Users/kazybektattibek/PycharmProjects/finlalproject/src/police_department.json', 'a') as file:
            json.dump(data, file, indent=5)
            file.close()

    def main(self, search_name: str):
        html = self.make_request(search_name)
        soup = self.make_soup(html)
        people = self.get_complaints(soup)
        result = []
        for person in people:
            personal_info = self.get_general_info(person)
            complaint = self.get_detailed_info_about_complaints()
            main_info = {
                'info': personal_info,
                'complaint': complaint
            }

            # data = Result(info=personal_info, complaint=complaint).model_dump()
            result.append(main_info)
        self.write_to_file(result)
        return result


if __name__ == '__main__':
    crawler = Crawler()
    res = crawler.main('Sasha')
    from pprint import pprint

    pprint(res)
