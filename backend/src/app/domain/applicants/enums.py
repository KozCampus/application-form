from __future__ import annotations

from enum import StrEnum


class ApplicantStatus(StrEnum):
    received = "received"
    accepted = "accepted"


class ProfessionalInterest(StrEnum):
    event_organization = "Eseményszervezés"
    communication = "Kommunikáció"
    partnerships = "Partnerkapcsolatok"
    media = "Média"
    hr = "HR"
    legal = "Jogi terület"
    it_digital = "IT/Digitális infrastruktúra"
