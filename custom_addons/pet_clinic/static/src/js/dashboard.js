/** @odoo-module */

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class PetClinicDashboard extends Component {
    static template = "pet_clinic.Dashboard";
    static props = ["*"];

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            // Filters
            lokasi_id: false,
            date_from: this._getFirstDayOfMonth(),
            date_to: this._getToday(),
            // KPI
            visitationCount: 0,
            memberCount: 0,
            petCount: 0,
            doctorCount: 0,
            // Service section filter
            serviceFilter: "month",
            serviceData: [],
            // Penanganan section filter
            penangananFilter: "month",
            penangananData: [],
            // Today tables
            visitationsToday: [],
            appointmentsToday: [],
            // Notif
            notifData: [],
            // Locations
            locations: [],
        });

        onWillStart(async () => {
            await this._fetchLocations();
            await this._fetchDashboardData();
        });
    }

    _getToday() {
        const d = new Date();
        return d.toISOString().split("T")[0];
    }

    _getFirstDayOfMonth() {
        const d = new Date();
        d.setDate(1);
        return d.toISOString().split("T")[0];
    }

    async _fetchLocations() {
        const locations = await this.orm.searchRead(
            "pet_clinic.lokasi",
            [],
            ["id", "name"]
        );
        this.state.locations = locations;
    }

    async _fetchDashboardData() {
        // KPI Cards
        const visitationDomain = [];
        const appointmentDomain = [];
        const doctorDomain = [["active", "=", true]];
        const memberDomain = [["active", "=", true]];
        const petDomain = [["active", "=", true]];

        if (this.state.lokasi_id) {
            const lokasiId = parseInt(this.state.lokasi_id);
            visitationDomain.push(["lokasi_pemeriksaan", "=", lokasiId]);
            appointmentDomain.push(["location_id", "=", lokasiId]);
            doctorDomain.push(["lokasi_ids", "in", [lokasiId]]);
            // Filter members/pets by those who have visited this branch
            memberDomain.push(["pet_ids.visitation_ids.lokasi_pemeriksaan", "=", lokasiId]);
            petDomain.push(["visitation_ids.lokasi_pemeriksaan", "=", lokasiId]);
        }

        if (this.state.date_from) {
            visitationDomain.push(["date_start", ">=", this.state.date_from + " 00:00:00"]);
            appointmentDomain.push(["date", ">=", this.state.date_from + " 00:00:00"]);
        }
        if (this.state.date_to) {
            visitationDomain.push(["date_start", "<=", this.state.date_to + " 23:59:59"]);
            appointmentDomain.push(["date", "<=", this.state.date_to + " 23:59:59"]);
        }

        this.state.visitationCount = await this.orm.searchCount(
            "pet_clinic.visitation",
            visitationDomain
        );
        this.state.memberCount = await this.orm.searchCount(
            "pet_clinic.client",
            memberDomain
        );
        this.state.petCount = await this.orm.searchCount(
            "pet_clinic.pet",
            petDomain
        );
        this.state.doctorCount = await this.orm.searchCount(
            "pet_clinic.doctor",
            doctorDomain
        );

        // Service Data
        await this._fetchServiceData();
        // Penanganan Data
        await this._fetchPenangananData();
        // Today's tables
        await this._fetchTodayVisitations();
        await this._fetchTodayAppointments();
        // Notif
        await this._fetchNotifData();
    }

    async _fetchServiceData() {
        const domain = this._getDateDomain(this.state.serviceFilter);
        if (this.state.lokasi_id) {
            domain.push(["visitation_id.lokasi_pemeriksaan", "=", parseInt(this.state.lokasi_id)]);
        }
        const services = await this.orm.readGroup(
            "pet_clinic.service",
            domain,
            ["service_type"],
            ["service_type"]
        );
        this.state.serviceData = services.map((s, idx) => ({
            no: idx + 1,
            name: s.service_type ? s.service_type[1] : "Undefined",
            count: s.service_type_count || 0,
        }));
    }

    async _fetchPenangananData() {
        const domain = this._getDateDomain(this.state.penangananFilter);
        if (this.state.lokasi_id) {
            domain.push(["lokasi_pemeriksaan", "=", parseInt(this.state.lokasi_id)]);
        }
        const penanganan = await this.orm.readGroup(
            "pet_clinic.visitation",
            domain,
            ["penanganan", "state"],
            ["penanganan", "state"],
            { lazy: false }
        );
        this.state.penangananData = penanganan.map((p, idx) => ({
            no: idx + 1,
            penanganan: p.penanganan || "-",
            state: p.state || "-",
            count: p.__count || 0,
        }));
    }

    _getDateDomain(filter) {
        const today = new Date();
        let dateFrom;
        if (filter === "today") {
            dateFrom = this._getToday();
            return [
                ["create_date", ">=", dateFrom + " 00:00:00"],
                ["create_date", "<=", dateFrom + " 23:59:59"],
            ];
        } else if (filter === "month") {
            const d = new Date();
            d.setDate(1);
            dateFrom = d.toISOString().split("T")[0];
            return [
                ["create_date", ">=", dateFrom + " 00:00:00"],
                ["create_date", "<=", this._getToday() + " 23:59:59"],
            ];
        } else {
            const d = new Date();
            d.setMonth(0, 1);
            dateFrom = d.toISOString().split("T")[0];
            return [
                ["create_date", ">=", dateFrom + " 00:00:00"],
                ["create_date", "<=", this._getToday() + " 23:59:59"],
            ];
        }
    }

    async _fetchTodayVisitations() {
        const today = this._getToday();
        const domain = [
            ["date_start", ">=", today + " 00:00:00"],
            ["date_start", "<=", today + " 23:59:59"],
        ];
        if (this.state.lokasi_id) {
            domain.push(["lokasi_pemeriksaan", "=", parseInt(this.state.lokasi_id)]);
        }
        const visitations = await this.orm.searchRead(
            "pet_clinic.visitation",
            domain,
            ["name", "owner_id", "pet_id", "doctor_id", "lokasi_pemeriksaan", "date_start"],
            { limit: 20 }
        );
        this.state.visitationsToday = visitations;
    }

    async _fetchTodayAppointments() {
        const today = this._getToday();
        const domain = [
            ["date", ">=", today + " 00:00:00"],
            ["date", "<=", today + " 23:59:59"],
        ];
        if (this.state.lokasi_id) {
            domain.push(["location_id", "=", parseInt(this.state.lokasi_id)]);
        }
        const appointments = await this.orm.searchRead(
            "pet_clinic.appointment",
            domain,
            ["name", "owner_id", "pet_id", "doctor_id", "location_id", "date"],
            { limit: 20 }
        );
        this.state.appointmentsToday = appointments;
    }

    async _fetchNotifData() {
        const today = this._getToday();
        const visitDomain = [
            ["date_start", ">=", today + " 00:00:00"],
            ["date_start", "<=", today + " 23:59:59"],
        ];
        if (this.state.lokasi_id) {
            visitDomain.push(["lokasi_pemeriksaan", "=", parseInt(this.state.lokasi_id)]);
        }
        
        const visitCount = await this.orm.searchCount(
            "pet_clinic.visitation",
            visitDomain
        );
        const reminderCount = await this.orm.searchCount(
            "pet_clinic.notif_reminder",
            []
        );
        const memberDomain = [["active", "=", true]];
        if (this.state.lokasi_id) {
            memberDomain.push(["pet_ids.visitation_ids.lokasi_pemeriksaan", "=", parseInt(this.state.lokasi_id)]);
        }
        const memberCount = await this.orm.searchCount(
            "pet_clinic.client",
            memberDomain
        );
        this.state.notifData = [
            { name: "Notif Kunjungan", count: visitCount },
            { name: "Notif Reminder", count: reminderCount },
            { name: "Notif Member", count: memberCount },
        ];
    }

    // Event handlers
    onLokasiChange(ev) {
        this.state.lokasi_id = ev.target.value || false;
    }

    onDateFromChange(ev) {
        this.state.date_from = ev.target.value;
    }

    onDateToChange(ev) {
        this.state.date_to = ev.target.value;
    }

    async onProcessClick() {
        await this._fetchDashboardData();
    }

    async onServiceFilterChange(filter) {
        this.state.serviceFilter = filter;
        await this._fetchServiceData();
    }

    async onPenangananFilterChange(filter) {
        this.state.penangananFilter = filter;
        await this._fetchPenangananData();
    }

    // Navigation
    openVisitations() {
        this.action.doAction("pet_clinic.action_pet_clinic_visitation");
    }

    openMembers() {
        this.action.doAction("pet_clinic.action_pet_clinic_client");
    }

    openPets() {
        this.action.doAction("pet_clinic.action_pet_clinic_pet");
    }

    openDoctors() {
        this.action.doAction("pet_clinic.action_doctor");
    }
}

registry.category("actions").add("pet_clinic_dashboard", PetClinicDashboard);
