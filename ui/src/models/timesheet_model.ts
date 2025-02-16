export interface MedicationDate {
    date: string;
    time: string;
}

export type MedicationBe = Omit<Medication, 'dates'> & { dates: string[] };
export type TimesheetBe = Omit<TimeSheet, 'medications'> & { medications: MedicationBe[] };

export class Medication {
    id: string;
    dosage: string;
    advise: string;
    name: string;
    dates: MedicationDate[];

    constructor(medication: MedicationBe) {
        this.id = medication.id;
        this.dosage = medication.dosage;
        this.advise = medication.advise;
        this.name = medication.name;
        this.dates = medication.dates.map(date => {
            try {
                return Medication.splitDate(date);
            } catch (error) {
                console.error(`Invalid date string: ${date}`, error);
                return { date: "Invalid date", time: "Invalid time" };
            }
        });
    }

    static splitDate(date: string): MedicationDate {
        const [datePart, timePart] = date.split('T');
        if (!datePart || !timePart) {
            throw new Error("Invalid date format");
        }
        return {
            date: datePart,
            time: timePart
        };
    }
}

export class TimeSheet {
    id: string;
    user_id: string;
    medications: Medication[];
    start_date: string; // Date string
    end_date: string;   // Date string

    constructor(timesheet: TimesheetBe) {
        this.id = timesheet.id;
        this.user_id = timesheet.user_id;
        this.start_date = timesheet.start_date;
        this.end_date = timesheet.end_date;
        this.medications = timesheet.medications.map(med => new Medication(med));
    }
}


